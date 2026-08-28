from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from runtime.contracts import ContractError, validate_task_input
from runtime.fixture_adapter import FixtureAdapter
from runtime.path_boundary import PathBoundary, PathBoundaryError
from runtime.run_store import RunStore, RunStoreError
from runtime.state_machine import InvalidTransition, StateMachine


FIXTURES = Path(__file__).parent / "fixtures"


class P1RuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = FixtureAdapter(FIXTURES / "knowledge_bases.json")
        self.raw_task = {
            "knowledge_base": "fixture-kb-alpha",
            "ip": "示例甲",
            "topic": "纯虚构 fixture 选题",
            "references": ["fixture://reference/example-one"],
            "user_thoughts": "只验证 Run 身份，不生成内容",
        }

    def _resolved(self, raw_task: dict[str, object]):
        task = validate_task_input(raw_task)
        knowledge_base, ip = self.adapter.resolve(task["knowledge_base"], task["ip"])
        return task, knowledge_base, ip

    def test_identical_input_resumes_same_run(self) -> None:
        task, knowledge_base, ip = self._resolved(self.raw_task)
        with tempfile.TemporaryDirectory() as temporary:
            store = RunStore(temporary)
            first = store.create_or_resume(task, knowledge_base, ip)
            second = store.create_or_resume(task, knowledge_base, ip)

        self.assertTrue(first.created)
        self.assertFalse(second.created)
        self.assertEqual(first.run["run_id"], second.run["run_id"])
        self.assertEqual(first.run, second.run)

    def test_different_knowledge_base_creates_different_run(self) -> None:
        first_task, first_kb, first_ip = self._resolved(self.raw_task)
        second_raw = {**self.raw_task, "knowledge_base": "fixture-kb-beta"}
        second_task, second_kb, second_ip = self._resolved(second_raw)
        with tempfile.TemporaryDirectory() as temporary:
            store = RunStore(temporary)
            first = store.create_or_resume(first_task, first_kb, first_ip)
            second = store.create_or_resume(second_task, second_kb, second_ip)

        self.assertNotEqual(first.run["run_id"], second.run["run_id"])
        self.assertNotEqual(
            first.run["knowledge_base_identity"], second.run["knowledge_base_identity"]
        )

    def test_different_ip_creates_different_run(self) -> None:
        first_task, knowledge_base, first_ip = self._resolved(self.raw_task)
        second_raw = {**self.raw_task, "ip": "示例乙"}
        second_task, second_kb, second_ip = self._resolved(second_raw)
        with tempfile.TemporaryDirectory() as temporary:
            store = RunStore(temporary)
            first = store.create_or_resume(first_task, knowledge_base, first_ip)
            second = store.create_or_resume(second_task, second_kb, second_ip)

        self.assertNotEqual(first.run["run_id"], second.run["run_id"])
        self.assertNotEqual(first.run["ip_identity"], second.run["ip_identity"])

    def test_none_ip_is_explicit_and_frozen(self) -> None:
        raw = {**self.raw_task, "ip": "无IP"}
        task, knowledge_base, ip = self._resolved(raw)
        with tempfile.TemporaryDirectory() as temporary:
            result = RunStore(temporary).create_or_resume(task, knowledge_base, ip)

        self.assertEqual(result.run["task_input"]["ip"], "none")
        self.assertEqual(result.run["ip_identity"]["status"], "none")
        self.assertIsNone(result.run["ip_identity"]["resolved_ref"])

    def test_two_waiting_states_cannot_be_skipped(self) -> None:
        self.assertEqual(StateMachine.WAITING_STATES, {"waiting_direction", "waiting_final"})
        with self.assertRaises(InvalidTransition):
            StateMachine.require_transition("direction_working", "direction_approved")
        with self.assertRaises(InvalidTransition):
            StateMachine.require_transition("draft_working", "final_approved")
        StateMachine.require_transition("direction_working", "waiting_direction")
        StateMachine.require_transition("draft_working", "waiting_final")
        with self.assertRaises(InvalidTransition):
            StateMachine.require_transition("waiting_direction", "direction_approved")
        with self.assertRaises(InvalidTransition):
            StateMachine.require_transition("waiting_final", "final_approved")
        StateMachine.require_gate_approval("waiting_direction", "direction_approved")
        StateMachine.require_gate_approval("waiting_final", "final_approved")

    def test_run_store_persists_only_legal_transitions(self) -> None:
        task, knowledge_base, ip = self._resolved(self.raw_task)
        with tempfile.TemporaryDirectory() as temporary:
            store = RunStore(temporary)
            created = store.create_or_resume(task, knowledge_base, ip)
            with self.assertRaises(InvalidTransition):
                store.advance(created.run["run_id"], "direction_approved")
            working = store.advance(created.run["run_id"], "direction_working")
            waiting = store.advance(created.run["run_id"], "waiting_direction")
            with self.assertRaises(InvalidTransition):
                store.advance(created.run["run_id"], "direction_approved")
            approved = store.approve_gate(
                created.run["run_id"], "A", "确认方向"
            )

        self.assertEqual(working["status"], "direction_working")
        self.assertEqual(waiting["status"], "waiting_direction")
        self.assertEqual(approved["status"], "direction_approved")
        self.assertEqual(approved["gate_approvals"][0]["gate"], "A")

    def test_gate_rejects_ambiguous_or_wrong_decision(self) -> None:
        task, knowledge_base, ip = self._resolved(self.raw_task)
        with tempfile.TemporaryDirectory() as temporary:
            store = RunStore(temporary)
            created = store.create_or_resume(task, knowledge_base, ip)
            store.advance(created.run["run_id"], "direction_working")
            store.advance(created.run["run_id"], "waiting_direction")
            with self.assertRaisesRegex(RunStoreError, "not an explicit approval"):
                store.approve_gate(created.run["run_id"], "A", "可以")

    def test_path_boundary_rejects_absolute_and_parent_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            boundary = PathBoundary(temporary)
            with self.assertRaises(PathBoundaryError):
                boundary.child("/tmp/outside")
            with self.assertRaises(PathBoundaryError):
                boundary.child("..", "outside")

    def test_contract_rejects_missing_ip_and_more_than_five_references(self) -> None:
        with self.assertRaises(ContractError):
            validate_task_input({"knowledge_base": "fixture-kb-alpha"})
        with self.assertRaises(ContractError):
            validate_task_input(
                {
                    "knowledge_base": "fixture-kb-alpha",
                    "ip": "none",
                    "references": [f"fixture://reference/{index}" for index in range(6)],
                }
            )

    def test_fixture_catalog_contains_no_absolute_customer_paths(self) -> None:
        catalog_text = (FIXTURES / "knowledge_bases.json").read_text(encoding="utf-8")
        catalog = json.loads(catalog_text)
        self.assertNotIn("/Users/", catalog_text)
        self.assertNotIn("token", catalog_text.casefold())
        for entry in catalog["knowledge_bases"]:
            self.assertTrue(entry["ref"].startswith("fixture://"))
            for resolved_ref in entry["ips"].values():
                self.assertTrue(resolved_ref.startswith("fixture://"))


if __name__ == "__main__":
    unittest.main()
