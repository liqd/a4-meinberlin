# Audit subtasks vs this PR (errors / non-heading warnings)

Parent: [ST-1816 — Fix HTML Errors](https://app.asana.com/1/1175467295883992/task/1213806008749002) · workspace `1175467295883992`

Only subtasks that had **at least one Nu Html Checker error** (or a non–empty-heading warning still tracked here) are listed. Subtasks that documented **only** the empty-heading warning are omitted.

Legend: **Fixed** = addressed in this codebase. **Not fixed** = still open or out of scope.

---

### [1213806008749008](https://app.asana.com/1/1175467295883992/task/1213806008749008) — `mein.berlin.de/` (2 errors, 4 heading warnings in audit table)

- **Fixed (errors):** `aria-valuemax` (and related redundant ARIA) with native `max` on `<progress>`; `<label>` descendant of `<a>` (module status bar inside project module tiles).
- **Not fixed (warnings):** “Article lacks heading” for homepage icon-list-style blocks (not changed here; markup differs from `icon_block` / needs CMS or other follow-up).

### [1213806008749011](https://app.asana.com/1/1175467295883992/task/1213806008749011) — Parkweißensee project

- **Fixed (errors):** invalid `id` / `for` from unexpanded `{{ module.pk }}` in progress markup; `aria-valuemax` with `max`; `<label>` inside `<a>` (same module status bar partial).
- **Not fixed:** —

### [1213806008749012](https://app.asana.com/1/1175467295883992/task/1213806008749012) — Parkweißensee `/information/`

- **Fixed (errors):** `aria-labelledby="contact-title"` with no matching `id` (added `id="contact-title"` on the contact `<h2>` in `project_information.html`).
- **Not fixed:** —

### [1213806008749014](https://app.asana.com/1/1175467295883992/task/1213806008749014) — Regionalkasse Marienfelde (first URL)

- **Fixed (errors):** same module status bar bundle as Parkweißensee project (invalid `id`/`for`, redundant ARIA, `label` in `a`).
- **Not fixed:** —

### [1213806008749015](https://app.asana.com/1/1175467295883992/task/1213806008749015) — Regionalkasse (second URL)

- **Fixed (errors):** same module status bar partial as other project pages (as far as that URL renders running modules with the tile).
- **Not fixed:** —

### [1213806008749016](https://app.asana.com/1/1175467295883992/task/1213806008749016) — `/accounts/signup/`

- **Fixed (errors):** non-standard `combined_answer_id` on the Captcheck container → `data-combined-answer-id` + JS; `label for` pointing at a hidden captcha control → label replaced with a non-`for` label for hidden widgets in `form_field.html`.
- **Not fixed:** —

### Plan detail pages (same contact block as story; no separate URL subtask in the list)

- **Fixed (errors):** `aria-labelledby="contact-title"` without target (`id="contact-title"` on contact `<h2>` in `plan_detail.html`).
- **Not fixed:** —

---

### Empty heading (`<h3 class="heading"></h3>`)

Not mapped to individual subtasks here. **We no longer reproduce this warning in the repo templates** (see `test_no_empty_heading_with_class_heading_in_templates`), and we **treat it as resolved** for our shipped markup (remaining cases on production, if any, are likely from third-party or non-template sources until re-validated).

---

### Meta / process subtasks (Info, Subtasks, a11y checklist, docs, UI testing, manual testing)

No direct mapping to specific Nu Html Checker **errors**; **Fixed / Not fixed** not applicable here.
