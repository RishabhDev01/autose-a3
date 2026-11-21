"""Issue 3: Table.pluck(field) returns that field's values, skipping docs without it."""


def test_pluck_returns_values_in_insertion_order(any_db):
    any_db.insert_multiple([{'name': 'a'}, {'name': 'b'}, {'name': 'c'}])
    assert any_db.pluck('name') == ['a', 'b', 'c']


def test_pluck_skips_documents_without_field(any_db):
    any_db.insert_multiple([{'name': 'a'}, {'age': 3}, {'name': 'c'}])
    assert any_db.pluck('name') == ['a', 'c']


def test_pluck_on_empty_table_and_named_table(any_db):
    assert any_db.pluck('name') == []
    users = any_db.table('users')
    users.insert({'email': 'x@y.z'})
    assert users.pluck('email') == ['x@y.z']
    assert any_db.pluck('email') == []
