"""Positive/negative tests for claims and trace envelopes, not game mechanics."""
import copy
import unittest

from validate_contracts import (ContractError, load_examples, validate_catalog,
                                validate_manifest, validate_trace)


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.manifest, self.catalog, self.events = load_examples()

    def test_examples(self):
        validate_catalog(self.catalog, self.manifest)
        validate_trace(self.events, self.manifest)

    def test_empty_trace_rejected(self):
        with self.assertRaisesRegex(ContractError, "must contain events"):
            validate_trace([], self.manifest)

    def test_unsupported_exit_cannot_certify_engine_comparison(self):
        self.manifest.update(claim="engine_differential",
                             binary={"sha256": "a" * 64, "relation": "matched"},
                             rules={"mode": "effective_export", "digest": "b" * 64, "module_order": []},
                             capabilities={"fixture_transition": "engine_recorded"},
                             engine_reference="synthetic-test-reference")
        # First validate the claim envelope; no actual engine evidence is implied.
        validate_trace(self.events, self.manifest)
        self.events[-1]["detail"]["outcome"] = "unsupported"
        with self.assertRaisesRegex(ContractError, "Unsupported event"):
            validate_trace(self.events, self.manifest)

    def test_old_binary_cannot_certify_current_source(self):
        self.manifest["claim"] = "engine_differential"
        self.manifest["binary"] = {"sha256": "a" * 64, "relation": "older"}
        with self.assertRaises(ContractError):
            validate_manifest(self.manifest)

    def test_matching_build_is_not_enough_without_rules_and_reference(self):
        self.manifest["claim"] = "engine_differential"
        self.manifest["binary"] = {"sha256": "a" * 64, "relation": "matched"}
        with self.assertRaises(ContractError):
            validate_manifest(self.manifest)

    def test_unbuilt_binary_cannot_have_hash(self):
        self.manifest["binary"]["sha256"] = "a" * 64
        with self.assertRaises(ContractError):
            validate_manifest(self.manifest)

    def test_unknown_envelope_field_rejected(self):
        self.manifest["silently_assume_path_success"] = True
        with self.assertRaises(ContractError):
            validate_manifest(self.manifest)

    def test_duplicate_scenario_id_rejected(self):
        self.catalog["scenarios"].append(copy.deepcopy(self.catalog["scenarios"][0]))
        with self.assertRaises(ContractError):
            validate_catalog(self.catalog, self.manifest)

    def test_gap_in_trace_sequence_rejected(self):
        self.events[2]["seq"] = 99
        with self.assertRaises(ContractError):
            validate_trace(self.events, self.manifest)

    def test_wrong_parent_rejected(self):
        self.events[2]["parent_span_id"] = None
        with self.assertRaises(ContractError):
            validate_trace(self.events, self.manifest)

    def test_parent_cannot_exit_while_child_active(self):
        self.events[5]["span_id"] = "root"
        self.events[5]["parent_span_id"] = None
        with self.assertRaises(ContractError):
            validate_trace(self.events, self.manifest)

    def test_partial_callback_effects_then_caught_exception_are_valid(self):
        self.assertEqual([e["type"] for e in self.events[3:6]], ["mutation", "exception", "exit"])
        validate_trace(self.events, self.manifest)

    def test_rng_wrong_value_rejected(self):
        self.events[1]["detail"]["value"] += 1
        with self.assertRaises(ContractError):
            validate_trace(self.events, self.manifest)

    def test_native_zero_bound_still_advances_seed(self):
        detail = self.events[1]["detail"]
        detail.update(supplied_bound=65536, native_bound=0, value=0)
        validate_trace(self.events, self.manifest)
        detail["after_u32"] = detail["before_u32"]
        with self.assertRaises(ContractError):
            validate_trace(self.events, self.manifest)

    def test_rng_stream_cannot_restart_silently(self):
        self.events.insert(2, copy.deepcopy(self.events[1]))
        for i, event in enumerate(self.events):
            event["seq"] = i
        with self.assertRaises(ContractError):
            validate_trace(self.events, self.manifest)

    def test_unclosed_span_rejected(self):
        with self.assertRaises(ContractError):
            validate_trace(self.events[:-1], self.manifest)

    def test_checkpoint_inside_callback_rejected(self):
        self.events[3].update(type="checkpoint", phase="checkpoint", span_id=None, parent_span_id=None,
                              detail={"state_digest": "a" * 64, "scope": "partial", "boundary": "quiescent"})
        with self.assertRaises(ContractError):
            validate_trace(self.events, self.manifest)

    def test_quiescent_checkpoint_valid(self):
        event = dict(self.events[-1], seq=len(self.events), type="checkpoint", phase="checkpoint",
                     span_id=None, parent_span_id=None,
                     detail={"state_digest": "a" * 64, "scope": "partial", "boundary": "quiescent"})
        self.events.append(event)
        validate_trace(self.events, self.manifest)


if __name__ == "__main__":
    unittest.main(verbosity=2)
