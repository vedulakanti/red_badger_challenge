import pytest
from scripts.analysis import calculate_human_proportion


def test_calculate_human_proportion():
    result = calculate_human_proportion("data/swapi/characters.csv", "data/swapi/species.csv")
    assert result is not None
    assert "human_proportion" in result
    assert "non_human_proportion" in result
