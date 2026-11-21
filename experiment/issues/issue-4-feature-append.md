---
type: feature
title: "Feature: an operation to append a value to a list field"
---

TinyDB has nice operations like `increment`, `add` and `delete` for `db.update(...)`. What I'm missing is one for lists. I store tags as a list and to add a tag I currently have to do

```python
def add_tag(doc):
    doc['tags'].append('urgent')
db.update(add_tag, Query().id == 7)
```

It would be great to have

```python
from tinydb.operations import append
db.update(append('tags', 'urgent'), Query().id == 7)
```

If the document doesn't have the field yet, it should start a new list with that one value (so I don't have to initialise `tags: []` on every insert).
