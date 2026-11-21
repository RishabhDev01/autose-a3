"""Issue 2: string document IDs must be handled consistently."""


def _seed(db):
    db.insert({'name': 'a'})
    db.insert({'name': 'b'})


def test_remove_accepts_string_ids(any_db):
    _seed(any_db)
    removed = any_db.remove(doc_ids=['1'])
    assert removed == [1]
    assert [d['name'] for d in any_db.all()] == ['b']


def test_update_accepts_string_ids(any_db):
    _seed(any_db)
    updated = any_db.update({'x': 1}, doc_ids=['2'])
    assert updated == [2]
    assert any_db.get(doc_id=2) == {'name': 'b', 'x': 1}


def test_get_with_string_id_returns_int_doc_id(any_db):
    _seed(any_db)
    doc = any_db.get(doc_id='1')
    assert doc == {'name': 'a'}
    assert doc.doc_id == 1
    assert isinstance(doc.doc_id, int)


def test_int_ids_still_work(any_db):
    _seed(any_db)
    assert any_db.remove(doc_ids=[2]) == [2]
    assert any_db.contains(doc_id=1)
    assert not any_db.contains(doc_id=2)
