"""Issue 4: operations.append(field, value) for list fields."""
from tinydb import Query


def test_append_to_existing_list(any_db):
    from tinydb.operations import append
    any_db.insert({'id': 7, 'tags': ['a']})
    any_db.update(append('tags', 'urgent'), Query().id == 7)
    assert any_db.get(Query().id == 7)['tags'] == ['a', 'urgent']


def test_append_creates_list_when_field_missing(any_db):
    from tinydb.operations import append
    any_db.insert({'id': 7})
    any_db.update(append('tags', 'urgent'), Query().id == 7)
    assert any_db.get(Query().id == 7)['tags'] == ['urgent']


def test_append_only_touches_matching_documents(any_db):
    from tinydb.operations import append
    any_db.insert({'id': 1, 'tags': []})
    any_db.insert({'id': 2, 'tags': []})
    any_db.update(append('tags', 'x'), Query().id == 2)
    assert any_db.get(Query().id == 1)['tags'] == []
    assert any_db.get(Query().id == 2)['tags'] == ['x']
