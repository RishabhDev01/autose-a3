---
type: vague
title: "search() gives me different data the second time??"
---

Something weird is going on. I search for a user, change something on the result in my code (I don't save it back, I'm just preparing it for display), and the next time I search, the result already has my change in it. Sometimes even `db.all()` shows the change. I never called `update`!

Is this a bug? It feels really unsafe, I had a bug in production because of it. Can search results be made safer somehow?
