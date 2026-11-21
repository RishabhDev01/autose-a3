---
type: bug
title: "update() with increment() half-applies when one document is missing the field"
---

Hi, I think I found a data consistency problem.

I use TinyDB with `MemoryStorage` in my tests and with a JSON file in production. I have a few documents and some of them don't have a `count` field yet. When I run

```python
from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from tinydb.operations import increment

db = TinyDB(storage=MemoryStorage)
db.insert({'count': 1})
db.insert({'other': 0})
db.insert({'count': 5})

db.update(increment('count'))   # KeyError: 'count'  (ok, fair enough)
print(db.all())
```

I get the KeyError, which is fine. But afterwards the first document has `count: 2`! So the update was half applied even though it failed. When I do the exact same thing with a JSON file, nothing is changed after the error, which is what I'd expect.

So the in-memory database and the file database behave differently. I would expect a failed update to leave the database exactly like it was before, no matter which storage I use.

TinyDB 4.9.0, Python 3.12.
