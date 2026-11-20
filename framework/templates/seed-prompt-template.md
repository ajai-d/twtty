# 📘 Seed Prompt Template

---

## 🗺️ Template

```markdown
## What I Want To Build

[Describe your project in plain language. What does it do? Who is it for?]

## Done Looks Like

[How will you know it's complete? What's the minimum viable outcome?]
```

---

## ▶️ What To Do

1. Copy the template above
2. Fill in "What I Want To Build" and "Done Looks Like"
3. Save it to `<project-folder>/seed/seed.md`
4. Give it to your AI agent with: *"Read `framework/methodology/core-twtty-methodology.md` and follow the TWTTY methodology."*

> **Project seed vs. Iteration Intent.** This file is your **project seed**
> (`seed/seed.md`) — the enduring, project-level intent. It drives the
> **baseline buildout** (the project's initial end-to-end build, unnumbered).
> Each later **iteration** then gets its own lightweight **Iteration Intent**
> (`seed/intent-<iteration-id>.md`) — a short statement of *what this increment
> adds, changes, or fixes* — drafted with you at the start of that iteration's
> SEED stage. You author the project seed once; the AI agent captures each
> Iteration Intent with you as the project progresses.

---

## 📝 Example (filled in)

```markdown
## What I Want To Build

A web application for submitting and tracking team work requests.

## Done Looks Like

- Users can submit a request with a title and description
- Users can view requests and update their status
- All tests pass
- Anyone can clone and run it locally
```