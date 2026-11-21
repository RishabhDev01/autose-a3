---
type: feature
title: "Feature: get a list of one field from all documents"
---

I often need just one field from every document, for example every `name`. Right now I write

```python
names = [d['name'] for d in db.all()]
```

but this crashes with a KeyError as soon as one document doesn't have a `name`, so I end up writing `d.get('name')` and then filtering out the Nones, every time.

Could TinyDB have something like

```python
db.pluck('name')   # -> ['a', 'b', ...]
```

that returns the values of that field for all documents in the table (in the order they were inserted) and just skips documents that don't have the field? It should also work on other tables: `db.table('users').pluck('email')`.
