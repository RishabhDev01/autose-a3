"""Issue 5 (vague): changing a returned document must not change stored or cached data.

Intended reading: results returned by search()/get()/all() are independent
copies. Mutating them, at the top level or in nested values, must not leak
into later reads.
"""
from tinydb import Query


def test_top_level_mutation_does_not_leak_into_next_search(any_db):
    any_db.insert({'name': 'alice', 'role': 'user'})
    first = any_db.search(Query().name == 'alice')
    first[0]['role'] = 'admin'
    again = any_db.search(Query().name == 'alice')
    assert again[0]['role'] == 'user'


def test_nested_mutation_does_not_leak_into_storage(any_db):
    any_db.insert({'name': 'alice', 'prefs': {'theme': 'light'}})
    doc = any_db.search(Query().name == 'alice')[0]
    doc['prefs']['theme'] = 'dark'
    assert any_db.all()[0]['prefs']['theme'] == 'light'
    assert any_db.search(Query().name == 'alice')[0]['prefs']['theme'] == 'light'


def test_get_result_mutation_does_not_leak(any_db):
    any_db.insert({'name': 'bob', 'tags': ['a']})
    any_db.get(Query().name == 'bob')['tags'].append('b')
    assert any_db.get(Query().name == 'bob')['tags'] == ['a']
