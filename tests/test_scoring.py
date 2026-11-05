"""Contract tests for scoring — EXPECTED RED until you implement on Nov 5.

These encode the spec: weights validation + feature/score contracts.
Run `make test` after implementing scoring.py and turn them green.
"""

import pytest

from relaydesk.scoring import ScoringError, load_weights

GOOD = {
    "error_symptom_match": 0.35,
    "component_version_match": 0.25,
    "release_timing_match": 0.20,
    "reproduction_evidence": 0.20,
}


def test_load_weights_round_trip():
    assert load_weights({"weights": GOOD}) == GOOD


def test_rejects_weights_that_do_not_sum_to_one():
    bad = dict(GOOD, error_symptom_match=0.55)
    with pytest.raises(ScoringError):
        load_weights({"weights": bad})


def test_rejects_negative_weight():
    bad = dict(GOOD, release_timing_match=-0.10)
    with pytest.raises(ScoringError):
        load_weights({"weights": bad})


def test_rejects_missing_feature_key():
    bad = {k: v for k, v in GOOD.items() if k != "release_timing_match"}
    with pytest.raises(ScoringError):
        load_weights({"weights": bad})
