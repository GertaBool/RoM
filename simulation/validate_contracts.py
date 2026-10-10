#!/usr/bin/env python3
"""Validate interchange examples; this does not execute game scenarios."""
import json
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
SCHEMA = json.loads((HERE / "contract.schema.json").read_text())
Draft202012Validator.check_schema(SCHEMA)
VALIDATOR = Draft202012Validator(SCHEMA)


class ContractError(ValueError):
    pass


def validate_envelope(value):
    errors = list(VALIDATOR.iter_errors(value))
    if errors:
        raise ContractError(errors[0].message)


def validate_manifest(manifest):
    validate_envelope(manifest)
    if manifest["kind"] != "manifest":
        raise ContractError("Expected a manifest")
    binary = manifest["binary"]
    if binary["relation"] == "unbuilt" and binary["sha256"] is not None:
        raise ContractError("An unbuilt binary cannot have a produced-binary hash")
    if binary["relation"] == "matched" and binary["sha256"] is None:
        raise ContractError("A matched build requires its binary hash")
    if manifest["claim"] == "engine_differential":
        if binary["relation"] != "matched" or not manifest["engine_reference"]:
            raise ContractError("Engine comparison requires a matching build and reference")
        if manifest["rules"]["mode"] != "effective_export" or not manifest["rules"]["digest"]:
            raise ContractError("Engine comparison requires identified effective rules")
        if any(v in ("modeled", "unsupported") for v in manifest["capabilities"].values()):
            raise ContractError("Declared engine-comparison capabilities cannot be modeled or unsupported")


def validate_catalog(catalog, manifest):
    validate_manifest(manifest)
    validate_envelope(catalog)
    if catalog["kind"] != "scenario_catalog":
        raise ContractError("Expected a scenario catalog")
    seen = set()
    for scenario in catalog["scenarios"]:
        if scenario["id"] in seen:
            raise ContractError("Duplicate scenario ID")
        seen.add(scenario["id"])
        if scenario["manifest_id"] != manifest["run_id"]:
            raise ContractError("Scenario references a different manifest")
        if scenario["status"] != "planned" and not scenario["evidence"]:
            raise ContractError("An evidence-available scenario needs evidence references")
        if scenario["status"] == "engine_evidence_available" and manifest["claim"] != "engine_differential":
            raise ContractError("Engine evidence must use the matching engine experiment")


def validate_trace(events, manifest):
    """Check sequence, nested spans, claim limits and source-derived RNG records.

    This is an envelope validator, not an effect interpreter: it does not check
    whether a mutation's old value matches a full world snapshot, nor whether a
    phase transition matches CvGame. Those require later simulator milestones.
    """
    validate_manifest(manifest)
    stack = []
    seen_spans = set()
    seeds = {}
    count = 0
    for seq, event in enumerate(events):
        count += 1
        validate_envelope(event)
        if event["kind"] != "trace_event":
            raise ContractError("Expected a trace event")
        if event["seq"] != seq or event["run_id"] != manifest["run_id"]:
            raise ContractError("Trace sequence or run identity mismatch")
        event_type = event["type"]
        span = event["span_id"]
        parent = event["parent_span_id"]
        if event_type == "enter":
            if span is None or span in seen_spans:
                raise ContractError("Span IDs must be nonnull and unique")
            if parent != (stack[-1][0] if stack else None):
                raise ContractError("Entry parent is not the active span")
            seen_spans.add(span)
            stack.append((span, parent))
        elif event_type == "checkpoint":
            if stack or span is not None or parent is not None:
                raise ContractError("Checkpoint requires a quiescent boundary")
            if event["phase"] != "checkpoint":
                raise ContractError("Checkpoint phase must be explicit")
        else:
            if not stack or (span, parent) != stack[-1]:
                raise ContractError("Event is outside its active span")
            if event_type == "exit":
                stack.pop()
        if event_type == "rng":
            detail = event["detail"]
            bound = detail["supplied_bound"] & 0xFFFF
            after = (1103515245 * detail["before_u32"] + 12345) & 0xFFFFFFFF
            expected = (((after >> 16) & 0xFFFF) * bound) // 65536
            if (detail["native_bound"], detail["after_u32"], detail["value"]) != (bound, after, expected):
                raise ContractError("RNG record differs from the source-derived 32-bit recurrence")
            stream = detail["stream"]
            if stream in seeds and seeds[stream] != detail["before_u32"]:
                raise ContractError("RNG stream continuity mismatch")
            seeds[stream] = after
        unsupported = event_type == "unsupported" or (
            event_type == "exit" and event["detail"]["outcome"] == "unsupported")
        if unsupported and manifest["claim"] == "engine_differential":
            raise ContractError("Unsupported event invalidates this engine-comparison claim")
    if not count:
        raise ContractError("A complete trace must contain events")
    if stack:
        raise ContractError("Trace ends with unclosed spans")


def load_examples():
    manifest = json.loads((HERE / "manifest.example.json").read_text())
    catalog = json.loads((HERE / "scenarios.json").read_text())
    events = [json.loads(line) for line in (HERE / "trace.example.jsonl").read_text().splitlines() if line]
    return manifest, catalog, events


def main():
    manifest, catalog, events = load_examples()
    validate_manifest(manifest)
    validate_catalog(catalog, manifest)
    validate_trace(events, manifest)
    print("Validated source-only manifest, %d scenario specifications and %d synthetic trace records."
          % (len(catalog["scenarios"]), len(events)))
    print("No game scenario or engine replay was executed.")


if __name__ == "__main__":
    main()
