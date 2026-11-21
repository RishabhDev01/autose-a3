"""Issue 1: a failed update() must leave the database unchanged."""
import pytest

from tinydb import Query
from tinydb.operations import increment


def _seed(db):
    db.insert({'count': 1})
    db.insert({'other': 0})
    db.insert({'count': 5})


def test_failed_update_leaves_data_unchanged(any_db):
    _seed(any_db)
    before = [dict(d) for d in any_db.all()]
    with pytest.raises(KeyError):
        any_db.update(increment('count'))
    assert [dict(d) for d in any_db.all()] == before


def test_failed_update_does_not_poison_query_cache(any_db):
    _seed(any_db)
    assert len(any_db.search(Query().count == 2)) == 0
    with pytest.raises(KeyError):
        any_db.update(increment('count'))
    assert any_db.search(Query().count == 2) == []
    assert any_db.count(Query().count == 1) == 1


def test_successful_update_still_applies(any_db):
    _seed(any_db)
    any_db.update(increment('count'), Query().count.exists())
    assert sorted(d['count'] for d in any_db.search(Query().count.exists())) == [2, 6]
