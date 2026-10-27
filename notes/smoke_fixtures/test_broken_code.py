"""Unit tests for calculate_priority_score."""
import pytest
from broken_code import calculate_priority_score

def test_standard_tier():
    assert calculate_priority_score(5, "standard") == 5

def test_enterprise_tier():
    assert calculate_priority_score(5, "enterprise") == 10

def test_vip_tier():
    assert calculate_priority_score(4, "vip") == 12

def test_default_fallback():
    assert calculate_priority_score(3, "community") == 3
