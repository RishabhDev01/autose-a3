---
type: bug
title: "remove(doc_ids=['1']) silently does nothing, but get(doc_id='1') works"
---

I'm building a small Flask app and the document IDs come in from the URL, so they are strings like `'1'`.

```python
db.insert({'name': 'a'})        # doc_id 1

db.get(doc_id='1')               # -> {'name': 'a'}   works!
db.remove(doc_ids=['1'])         # -> []   nothing removed?!
db.update({'x': 1}, doc_ids=['1'])  # -> []   nothing updated
```

`get` finds the document with a string ID, but `remove` and `update` just return an empty list and don't touch anything. No error, so I only noticed when the document was still there.

Also the document I get back from `db.get(doc_id='1')` has `doc_id == '1'` (a string) while every other document has an int `doc_id`, which broke a comparison in my code.

Either all of them should accept `'1'` or none of them should. I'd prefer they all accept it, since `get` already does.
