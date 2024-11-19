import os
import pytest
from scripts.fetch_swapi_data import fetch_data, save_data


def test_fetch_data():
    data = fetch_data("people/")
    assert isinstance(data, list)
    assert len(data) > 0


def test_save_data():
    data = [{"name": "Luke Skywalker", "species": ["human"]}]
    save_data(data, "test_characters.csv")
    assert os.path.exists("data/test_characters.csv")
