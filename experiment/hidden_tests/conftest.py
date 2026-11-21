"""Shared fixtures for the hidden acceptance tests.

These tests live OUTSIDE the fork, so the agents never see them. To run them
against a branch, copy this folder into the fork checkout and run:

    python -m pytest -q -p no:cacheprovider -o addopts="" hidden_tests/
"""
import pytest

from tinydb import TinyDB
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage, MemoryStorage


@pytest.fixture(params=['memory', 'json', 'caching'])
def any_db(request, tmp_path):
    if request.param == 'memory':
        db = TinyDB(storage=MemoryStorage)
    elif request.param == 'json':
        db = TinyDB(tmp_path / 'db.json', storage=JSONStorage)
    else:
        db = TinyDB(storage=CachingMiddleware(MemoryStorage))
    yield db
    db.close()
