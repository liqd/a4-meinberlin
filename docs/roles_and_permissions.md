# Roles and permissions in meinBerlin

This document describes how access control works in meinBerlin **after the planned guest-user port**. It covers project-level rules (django-rules), guest users, and account/UI restrictions.

For the underlying framework concepts, see also [adhocracy4 roles and permissions](https://github.com/liqd/adhocracy4/blob/main/docs/roles_and_permissions.md). meinBerlin overrides several a4 defaults in [`meinberlin/apps/projects/rules.py`](../meinberlin/apps/projects/rules.py).

**Status:** design spec for review — guest-user behaviour is planned, not yet implemented.

---

## Roles

| Role | How assigned | Guest user? |
|------|----------------|-------------|
| **Admin** (superuser) | Django `is_superuser` | No |
| **Initiator** | User is in `organisation.initiators` | No |
| **Moderator** | User is in `project.moderators` | No |
| **Org group admin** | User belongs to the Django group assigned to the project (`project.group`) | No |
| **Project participant** | User accepted a private/semipublic invite (`project.participants`) | No (guests cannot accept invites without converting) |
| **Registered user** | Full account (email verified) | No |
| **Guest user** | Temporary account via `/accounts/guests/login/`; linked `Guest` record | Yes |
| **Anonymous** | Not logged in (`AnonymousUser`) | No |

Notes:

- meinBerlin does **not** use adhocracy-plus-style **organisation members** (`is_org_member`). Access beyond initiators/groups is via project visibility and participant invites.
- **Org group admins** are a meinBerlin-specific role: initiators can assign a Django auth group to a project. Users in that group can work on that project (and add projects for the organisation) without being full initiators of every project in the org.
- **Guest users are always ordinary participants.** They never hold initiator, moderator, org group admin, or org member roles.

---

## Project access levels

Projects have an `access` setting. meinBerlin offers all three levels in the dashboard ([`meinberlin/apps/dashboard/forms.py`](../meinberlin/apps/dashboard/forms.py), labels in [`meinberlin/apps/projects/overwrites.py`](../meinberlin/apps/projects/overwrites.py)):

| Access | Dashboard label (summary) | On Kiezradar / public listings | View content (live) | Participate (live) |
|--------|-------------------------|--------------------------------|---------------------|---------------------|
| `PUBLIC` | All users can see tile and content and can participate | Yes | Everyone | Everyone with an account (see module rules); limited anonymous paths below |
| `SEMIPUBLIC` | All users can see tile and content; **only invited users** can participate | Yes | Everyone | Invited participants + initiator / moderator / org group admin only |
| `PRIVATE` | Only invited users can see tile and content and can participate | No | Invitees + elevated roles | Same as view |

**Semipublic in plain terms:** open gallery, closed participation. Anyone can read what’s going on; only people explicitly invited to the project (plus staff roles) can post, vote, comment, etc. Module pages show: *“This project is publicly visible. Invited users can actively participate.”*

**Private in plain terms:** invite-only throughout — no public listing, no browsing by outsiders. Module pages show: *“This project is not publicly visible. Only invited users can see content and actively participate.”*

Projects also have:

- **`is_draft`** — unpublished; only elevated roles can view/participate.
- **`is_archived`** — ended/archived; view/participate rules still apply but modules may be in closed phases.
- **`allow_guest_users`** *(planned)* — per-project toggle (default `True`). When `False`, guest users cannot participate even on public projects. Set by initiators/org group admins in the dashboard project basic form.

---

## Project-level permissions (django-rules)

meinBerlin defines three project permissions in [`meinberlin/apps/projects/rules.py`](../meinberlin/apps/projects/rules.py). Module permissions (ideas, polls, budgeting, etc.) build on these via phase rules and `participate_in_project`.

### `a4projects.view_project`

Who can open the project (module pages, detail views):

```
superuser
| initiator
| moderator
| org_group_admin
| ((public OR semipublic OR project_participant) AND project_is_live)
```

| Role / case | Draft | Live public | Live semipublic | Live private |
|-------------|-------|-------------|-----------------|--------------|
| Anonymous | No | Yes | Yes | No |
| Registered user | No | Yes | Yes | No |
| Guest user | No | Yes | Yes | No |
| Project participant | No | Yes | Yes | Yes |
| Org group admin (project group) | Yes | Yes | Yes | Yes |
| Moderator | Yes | Yes | Yes | Yes |
| Initiator | Yes | Yes | Yes | Yes |
| Admin | Yes | Yes | Yes | Yes |

Guests follow the same **view** rules as anonymous and registered users. `allow_guest_users` does **not** affect viewing.

### `a4projects.participate_in_project`

**Project-level gate** — who may participate at all (module rules apply on top):

**Current rule:**

```
superuser
| initiator
| moderator
| org_group_admin
| ((public OR project_participant) AND project_is_live)
```

**Planned rule** (adds guest gating):

```
superuser
| initiator
| moderator
| org_group_admin
| ((public OR project_participant) AND project_is_live AND guest_may_participate)
```

`guest_may_participate` (from adhocracy4):

- Returns `True` for everyone who is **not** a guest user.
- For guest users, returns `project.allow_guest_users`.

| Role / case | Draft | Live public | Live public, guests disabled | Live semipublic | Live private |
|-------------|-------|-------------|------------------------------|-----------------|--------------|
| Anonymous | No | Yes* | Yes* | No | No |
| Registered user | No | Yes | Yes | No | No |
| Guest user | No | Yes | **No** | No | No |
| Project participant | No | Yes | Yes | Yes | Yes |
| Org group admin | Yes | Yes | Yes | Yes | Yes |
| Moderator | Yes | Yes | Yes | Yes | Yes |
| Initiator | Yes | Yes | Yes | Yes | Yes |
| Admin | Yes | Yes | Yes | Yes | Yes |

\* **Project rule only** — see [Project rule vs module rules](#project-rule-vs-module-rules) below. Anonymous users pass this gate on public live projects but most modules still require login.

Important:

- **Guest accounts** let visitors participate in normal modules (ideas, ratings, etc.) on public live projects **without** full email/password signup. Contributions are tied to a temporary account that can be converted later.
- On **semipublic** and **private** projects, guests have **no** participate access unless they are explicit project participants (which requires converting to a full account and accepting an invite).
- Elevated roles (initiator, moderator, org group admin) bypass `guest_may_participate` because guests never hold those roles.

Additionally, `Project.has_member()` in adhocracy4 blocks guests when `allow_guest_users=False` on public projects (used by `is_project_member` and related checks).

### Project rule vs module rules

`participate_in_project` is a coarse project gate. **Most modules add stricter checks** via `is_context_member`, which requires `user.is_authenticated` on public projects (`Project.has_member()`).

| Actor | Passes `participate_in_project` on public live? | Can add ideas / topics / most module content? |
|-------|-----------------------------------------------|-----------------------------------------------|
| Anonymous | Yes (project rule) | **No** — not authenticated |
| Guest user | Yes (if `allow_guest_users`) | **Yes** — authenticated |
| Registered user | Yes | **Yes** |

**Anonymous participation without any account** is limited to module-specific mechanisms (not general project participation):

| Mechanism | Module | How it works |
|-----------|--------|----------------|
| Live questions | `livequestions` | `add_livequestion` only checks active phase; no login. `AnonymousItem` — no stored user creator. |
| Unregistered poll voters | `polls` | On **public** polls with `allow_unregistered_users=True`, browser gets a random `content_id`; votes stored without a user. |
| Token voting | `budgeting` (Kiezkasse) | User enters a one-time voting token; token hash stored in session. See [Token voting](#token-voting-budgeting--kiezkasse) below. |

Guest users are **not** a replacement for token voting or unregistered polls — they address the common case where someone wants to contribute to ideas, comments, ratings, etc. with a persistent identity but without registering.

### `a4projects.add_project` / `a4projects.change_project`

Inherited from adhocracy4 defaults (not overridden in meinBerlin):

- **Add project:** superuser, initiator, org group member (user in one of the organisation's groups).
- **Change project:** superuser, initiator (meinBerlin does not extend change to group admins on all projects — see tests in `tests/projects/rules/test_rules_add_change_delete.py`).

### `a4projects.delete_project`

meinBerlin custom rule:

```
superuser
| (initiator AND no_non_initiator_contributions)
```

Initiators may delete a project only if there are no contributions from non-initiators (ideas, comments, votes, poll answers, ratings). Org group admins and moderators cannot delete projects via this rule.

---

## Guest users (planned)

### Creation and session

1. Visitor opens `/accounts/guests/login/` (terms + captcha).
2. `django-guest-user` creates a temporary `User` + `Guest` record and logs the user in via session.
3. Guest usernames are auto-generated; placeholder emails use `guest-{uuid}@guest.invalid` (override library default).

### What guests can do

- Participate on **public, live** projects where `allow_guest_users=True`.
- View public and semipublic live projects (same as any visitor).
- Convert to a full account (`/account/guest/convert/`) — keeps contributions after email confirmation.

### What guests cannot do

- Delete their account via a dedicated flow (not in port — log out / close browser instead).

- Hold initiator, moderator, org group admin, or project participant roles.
- Participate when `allow_guest_users=False` on a project.
- Participate on semipublic or private projects (unless they become a project participant after converting).
- Access full account features (see Account/UI below).
- **Receive notifications or use notification features** (confirmed — see below).

### Notifications (confirmed)

Guest users must **not** access notifications UI/API/settings or receive **emails** while guest. **In-app `Notification` rows are still created** (same `User` pk) and become available after convert + email confirm.

| Surface | While guest | After convert |
|---------|-------------|---------------|
| `Notification` DB rows | **Created** (e.g. reply to guest's post) | Visible on notifications page |
| `/account/notifications/` | `RegularUserRequiredMixin` | Open |
| `/account/notification-settings/` | `RegularUserRequiredMixin` | Open |
| Header / hamburger notifications links | Hidden (`is_guest_user`) | Shown |
| `/api/notifications/` + settings API | Reject guests | Open |
| Outbound emails | Blocked (`_exclude_guest_users`) | Per `NotificationSettings` |

**Guest convert** newsletter/notification opt-in checkboxes apply after conversion and email confirmation.

**a+:** UI already blocks guests (`RegularUserRequiredMixin` on user dashboard, hidden bell). In-app rows already created. **Gap:** emails still sent to guests — see separate plan for a+ email fix.

### Terms of use (confirmed: site-wide only)

meinBerlin does **not** use per-project or per-organisation terms. Guest flows match regular signup:

| Flow | Terms handling |
|------|----------------|
| Guest create | Required `terms_of_use` checkbox + captcha; template links to `/terms-of-use` and `/datenschutz` with meinBerlin signup consent wording |
| Guest convert | Same site-wide `terms_of_use` checkbox again (as a+ does on convert, but with mB copy/URLs) |
| Guest account page | Convert form only — **no** delete tab, **no** user agreements page |

No `OrganisationTermsOfUse` model, views, or URLs.

### Admin control

The **only guest-specific setting** for project admins is **`allow_guest_users`** on the project basic form in the dashboard (visible when `A4_ENABLE_GUEST_USERS=True` in settings). Initiators and org group admins use this to allow or block guest participation per project.

---

## Account and UI restrictions (planned)

Guest users are `is_authenticated=True` in Django, so UI and API must explicitly gate guest-only vs regular-user features.

| Feature | Registered user | Guest user | Anonymous |
|---------|-----------------|------------|-----------|
| Login / register | Yes | Via guest create | Yes |
| Profile / password / email | Yes | No — convert first | No |
| Notification settings (React) | Yes | **No** (confirmed) | No |
| Notifications page (`/account/notifications/`) | Yes | **No** (confirmed) | No |
| Receive notification emails | Yes | **No** (confirmed) | No |
| Followed projects | Yes | **No** | No |
| Kiezradar browse/search (`/kiezradar/`) | Yes | **Yes** | Yes |
| Save search profile (inline on `/kiezradar/`) | Yes | **Hidden** | Login modal |
| Search profiles settings (`/account/search-profiles/`) | Yes | **No** (route lock) | No |
| Kiez Selection settings (`/account/kiezauswahl/`) | Yes | **No** (route lock) | No |
| Dashboard (initiator) | If initiator/group | No | No |
| Follow project (React widget) | Yes | **No** (hidden) | Redirect to login |
| Header login button | Logout | Guest settings / convert | Login |

Server-rendered views use `RegularUserRequiredMixin` (from `django-guest-user`) to block guests from regular account pages. Guest-specific pages use `GuestUserRequiredMixin`.

Session APIs (follows, notifications, search profiles, kiezradar filters) authenticate via **session cookie**, not JWT. APIs and email delivery must explicitly exclude guest users even though `is_authenticated=True`.

### Kiezradar (confirmed)

- **Main page** (`/kiezradar/`): guests may browse, filter, and search.
- **Settings pages** (`/account/search-profiles/`, `/account/kiezauswahl/`): `RegularUserRequiredMixin` — guests redirected to convert.
- **APIs** (`SearchProfileViewSet`, `KiezRadarViewSet`): `is_regular_user` in rules instead of `is_authenticated`.
- **Nav**: hide Searchprofiles and Kiez Selection links for guests.
- **Inline save button** on `/kiezradar/`: hide via explicit `isGuestUser` prop — do not render `SaveSearchProfile` for guests (`ProjectsControlBar`). Keep `isAuthenticated` for anonymous login modal only.

---

## Other participation patterns (unchanged by guest port)

These are separate from guest users and from normal logged-in participation.

### Token voting (budgeting / Kiezkasse)

Used in **participatory budgeting** modules where the process is designed for **offline or hybrid** voting — e.g. distributing physical cards with codes at an event, or giving residents a one-time digital token so each person can vote once without creating a platform account.

**How it works:**

1. **Initiators generate tokens** in the dashboard (`VotingToken`, grouped in `TokenPackage` per module). Tokens are random strings; only a salted hash is stored in the database ([`meinberlin/apps/votes/models.py`](../meinberlin/apps/votes/models.py)).
2. **Voter enters token** on the budgeting module page via `TokenForm` ([`meinberlin/apps/budgeting/views.py`](../meinberlin/apps/budgeting/views.py)).
3. On success, a **hash of the token** is stored in `request.session["voting_tokens"][module_id]` (expires after 12 hours; cleared by [`VotingTokenSessionMiddleware`](../meinberlin/apps/votes/middleware.py)).
4. During the **voting phase**, the session token authorises API calls to `TokenVoteViewSet` ([`meinberlin/apps/votes/api.py`](../meinberlin/apps/votes/api.py)) — votes are recorded as `TokenVote` linked to the `VotingToken`, not to a `User`.
5. Each token can only vote once per proposal/module (enforced on the token).

**No user account** is involved — not guest, not registered. This is independent of `participate_in_project` and of the guest-user port.

Typical contrast:

| | Guest user | Token voting |
|---|------------|--------------|
| Identity | Temporary `User` + session login | Anonymous session + token |
| Can post ideas / comment | Yes (public modules) | No — vote only |
| Persists across browser close | Until session ends (`SESSION_EXPIRE_AT_BROWSER_CLOSE`) | 12h session window |
| Convert to full account | Yes | N/A |

### Anonymous participation (no account)

See [Project rule vs module rules](#project-rule-vs-module-rules) for the live-questions, unregistered-poll, and token-voting cases.

### Phase and module rules

Even with `participate_in_project`, individual modules only allow actions during the correct **phase** (e.g. collect phase, voting phase). See [adhocracy4 phases and modules](https://github.com/liqd/adhocracy4/blob/main/docs/phases_and_modules.md).

---

## Source of truth in code

| Concern | Location |
|---------|----------|
| meinBerlin project rules override | [`meinberlin/apps/projects/rules.py`](../meinberlin/apps/projects/rules.py) |
| a4 predicates (`is_live`, `guest_may_participate`, …) | `adhocracy4/projects/predicates.py` |
| `allow_guest_users` field, `has_member` guest check | `adhocracy4/projects/models.py` |
| Dashboard toggle | `adhocracy4/dashboard/forms.py` + [`meinberlin/templates/a4dashboard/includes/project_basic_form.html`](../meinberlin/templates/a4dashboard/includes/project_basic_form.html) |
| Guest user library | `django-guest-user` |
| Behavioural tests | [`tests/projects/rules/`](../tests/projects/rules/) |

When in doubt, prefer the tests in `tests/projects/rules/` for meinBerlin-specific behaviour (especially initiator vs org group admin).

---

## Planned changes summary

1. Bump adhocracy4 to a build that includes guest support (see [Implementation notes](#implementation-notes-port) — do **not** pin `@main`).
2. Add the **`liqd/django-guest-user` fork** (a+ pins `@cfee4f0`), which already fixes guest creation for email-as-username models. One-time guest, no re-login, no account deletion.
3. Add `& guest_may_participate` to the public-participant branch of `participate_in_project`.
4. Enable `A4_ENABLE_GUEST_USERS` and render the dashboard `allow_guest_users` field.
5. Gate account, notification, and Kiezradar **settings** UI/API for guests; keep main Kiezradar browse/search open.
6. Exclude guests from outbound notification emails.

---

## Implementation notes (port)

Concrete notes per work item, derived from reading the current meinBerlin code, the a4 diff between `mB-v2606.3` (current pin) and `main`, and the `django-guest-user` source. **Open decisions are marked ⚠️.**

### Shared primitives (build these first)

- **`is_regular_user` rules predicate** — add to [`meinberlin/apps/users/predicates.py`](../meinberlin/apps/users/predicates.py):

```python
from adhocracy4.projects.guest_users import is_guest_user

@rules.predicate
def is_regular_user(user):
    return bool(user.is_authenticated) and not is_guest_user(user)
```

- **`IsRegularUser` DRF permission** — for viewsets that gate via `permission_classes` rather than rules (notifications). Wrap the predicate.
- **`RegularUserRequiredMixin`** — provided by `django-guest-user` (`guest_user.mixins`); use directly for server-rendered views. Redirects guests to the convert URL.

Use `adhocracy4.projects.guest_users.is_guest_user` everywhere (it safely returns `False` when the `guest_user` app is not installed, so the predicate is inert until the library is added).

### 1. adhocracy4 bump (`@main` for now — decided)

- **Decision:** point [`requirements/base.txt`](../requirements/base.txt) at `git+https://github.com/liqd/adhocracy4.git@main` (matches a+). Guest support is on `main` (`e8362f685`), 2 commits past `mB-v2606.3`.
- ⚠️ Caveat: those 2 commits also touch unrelated files (`polls/serializers.py`, `polls` JSX, `images/widgets.py`, `FormFieldError.jsx`, dashboard `form_field.html`), so run a **broad smoke/regression pass, not guest-only tests**. Revisit pinning a proper `mB-*` tag before release.
- Once bumped, a4 provides for free: `allow_guest_users` field + migration `0054`, `guest_may_participate` predicate, `Project.has_member()` guest check, `guest_users.is_guest_user`, and the `A4_ENABLE_GUEST_USERS`-gated field in a4's own `ProjectBasicForm`. **Note:** a4 also adds `& guest_may_participate` to *its* `participate_in_project` rule, but meinBerlin overrides that rule (see item 3), so a4's version does not take effect — meinBerlin must re-add it.

### Upstream / fork changes (a4 + django-guest-user)

Both dependencies are liqd-controlled and already carry the guest work for adhocracy-plus. meinBerlin can reuse them; the notes below list what (if anything) must change.

**adhocracy4 — no code change, release only.**

- All guest code lives on a4 `main` (2 commits past `mB-v2606.3`); a+ runs a4 `@main`. meinBerlin needs the **same commits cut as an `mB-*` tag** (or pin the SHA). No a4 source changes are required for meinBerlin.
- Caveat to confirm with liqd: a4's `ProjectBasicForm` puts `allow_guest_users` in `required_for_project_publish` whenever `A4_ENABLE_GUEST_USERS=True`. Model default is `True`, so publishing still works, but confirm this is the intended UX (field must be answered to publish).

**django-guest-user — use the `liqd/django-guest-user` fork.**

- a+ pins `git+https://github.com/liqd/django-guest-user.git@cfee4f0`. The fork is **1 commit ahead of upstream** ("add password and email for guest account"), which changes creation to:

```python
username = self.generate_username()
email = f"guest+{username}@liqd.net"
password = self.generate_password()
user = UserModel.objects.create_user(username, email, password)
```

  This **already resolves the email-as-username creation bug** (unique email + password), so the infinite-loop failure does not occur. meinBerlin should depend on this fork, **not** upstream `django-guest-user`.
- **Email domain: accepted `guest+{username}@liqd.net`** for now (deliverable address). This makes the guest email exclusion (item 6) **mandatory** — real mail must never be sent to these addresses.
- **Two fork bugs to patch** (owned by meinBerlin, needs a new pinned commit):
  - On `IntegrityError` the retry regenerates only `username`; re-derive `email` (and `password`) from the new username inside the loop.
  - If `create_guest_user(username=...)` is called with an explicit username, `email`/`password` are unbound → `NameError`; bind them in that path too.
- meinBerlin's `User` manager is plain `auth_models.UserManager`, so the fork's `create_user(username, email, password)` populates both the `username` and `email` fields correctly (positional `username`→`username` field, `email`→`email` field — meinBerlin has both columns).
- **Simplification vs the port plan:** because we accept the fork's `@liqd.net` email and both fields populate correctly, the custom swappable-`Guest`-model / `GuestManager.create_guest_user()` override that the port plan lists under `custom-guest-creation` is **likely unnecessary** — configure `NAME_GENERATOR` and use the fork as-is. ⚠️ Verify with a first-guest-creation test (two guests in a row, confirm no unique-constraint error). Only reintroduce an override if a `.invalid` domain is later required.

### 2. Guest creation & required settings

With the fork above, creation works; the remaining work is meinBerlin configuration and glue.

- **Settings** (mirror a+, in [`settings/base.py`](../meinberlin/config/settings/base.py)):
  - add `"guest_user"` to `INSTALLED_APPS` and `"guest_user.backends.GuestBackend"` to `AUTHENTICATION_BACKENDS`;
  - `A4_ENABLE_GUEST_USERS = True`;
  - `GUEST_USER = {"NAME_GENERATOR": "guest_user.functions.generate_numbered_username"}` (**decided: friendly `Guest####`**, e.g. `Guest4810`; `NAME_PREFIX`/`NAME_SUFFIX_DIGITS` default to `Guest`/`4`);
  - `GUEST_USER_REQUIRED_ANON_URL = "/accounts/guests/login"`, `GUEST_USER_CONVERT_URL = "/account/guest/convert/"`, `GUEST_USER_REQUIRED_USER_URL = "/account/profile/"`.
- **Convert form.** Default `CONVERT_FORM = guest_user.forms.UserCreationForm` does not match meinBerlin's User (email login + separate username + site-wide `terms_of_use` + captcha). Provide a meinBerlin form and set `GUEST_USER_CONVERT_FORM` — this is meinBerlin code, not a fork change.
- **Guest create view (explicit-only — decided).** `GUEST_USER_REQUIRED_ANON_URL` (`/accounts/guests/login`) needs a meinBerlin `GuestCreateView` + template with the terms checkbox + **reused signup captcha** (`CaptcheckCaptchaField`) that explicitly creates the guest. Do **not** use transparent `@allow_guest_user`/`AllowGuestUserMixin` auto-creation on participation views — creation happens only through this explicit page. No proactive "convert your account" nudging for now.
- Side effect (benign): [`meinberlin/apps/users/signals.py`](../meinberlin/apps/users/signals.py) auto-creates a `NotificationSettings` row for every new user, so guests get one with defaults — see item 6.

### 3. `participate_in_project` rule

- Re-add `& guest_may_participate` to the public branch in [`meinberlin/apps/projects/rules.py`](../meinberlin/apps/projects/rules.py) (meinBerlin overrides a4's rule via `rules.set_perm`).
- **Module content is gated automatically.** Ideas/comments/ratings/budgeting/polls resolve through a4's `is_context_member` → `is_project_member` → `Project.has_member()`, and `has_member` now returns `False` for guests when `allow_guest_users=False`. So no per-module rule edits are needed. ⚠️ Verify no meinBerlin module rule uses a raw `is_authenticated` in place of the module predicates.

### 4. Dashboard `allow_guest_users` field

- Set `A4_ENABLE_GUEST_USERS = True` in [`meinberlin/config/settings/base.py`](../meinberlin/config/settings/base.py). a4's `ProjectBasicForm` then adds the field (and lists it in `required_for_project_publish`; model default is `True`, so publishing is unaffected).
- meinBerlin **overrides** the template ([`meinberlin/templates/a4dashboard/includes/project_basic_form.html`](../meinberlin/templates/a4dashboard/includes/project_basic_form.html)) and it does not render the field — add a guarded block:

```django
{% if form.allow_guest_users %}
    {% include 'a4dashboard/includes/form_field.html' with field=form.allow_guest_users %}
{% endif %}
```

- meinBerlin does **not** subclass `ProjectBasicForm` (only `DashboardProjectCreateForm`), so the a4 form is used as-is for the basic settings component — no form class change needed.

### 5. API / server-view permission audit

Guests are session-authenticated, so **every `IsAuthenticated`/`is_authenticated` gate admits them** and DRF's default (`AllowAny`, no `DEFAULT_PERMISSION_CLASSES` set) admits everyone. Participation endpoints are fine (see item 3); the work is on **account/settings** surfaces.

**Must BLOCK guests — changes required:**

| Surface | File | Current gate | Change |
|---------|------|--------------|--------|
| `NotificationViewSet` (+ `interactions`, `followed_projects`, `search_profiles` actions) | [`apps/notifications/api.py`](../meinberlin/apps/notifications/api.py) | **none** (DRF default `AllowAny`) | add `permission_classes = [IsRegularUser]` |
| `NotificationSettingsViewSet` | [`apps/notifications/api.py`](../meinberlin/apps/notifications/api.py) | **none** | add `permission_classes = [IsRegularUser]` |
| `KiezRadarViewSet`, `SearchProfileViewSet` | [`apps/kiezradar/api.py`](../meinberlin/apps/kiezradar/api.py) | `ViewSetRulesPermission` → rules below | swap predicate in rules |
| `*_kiezradar`, `*_searchprofile` perms | [`apps/kiezradar/rules.py`](../meinberlin/apps/kiezradar/rules.py) | `rules.is_authenticated` / `is_authenticated_and_owner` | use `is_regular_user` (and `is_regular_user & is_owner`) |
| `FollowViewSet` (create/toggle follow) | a4 `follows/api.py`, registered in [`config/urls.py`](../meinberlin/config/urls.py) | `IsAuthenticated` | **Decided: hard-block.** Trivial — subclass with `permission_classes = [IsRegularUser]` and register the subclass at `r"follows"` instead of a4's. |
| `FollowedProjectsListViewSet` | [`apps/account/api.py`](../meinberlin/apps/account/api.py) | `AllowAny` (filters by user) | returns empty for guests; add `IsRegularUser` for consistency |
| `ProfileUpdateView`, `NotificationSettingsView`, `FollowedProjectsListView` | [`apps/account/views.py`](../meinberlin/apps/account/views.py) | `LoginRequiredMixin` | → `RegularUserRequiredMixin` |
| `NotificationsView` | [`apps/account/views.py`](../meinberlin/apps/account/views.py) | **no mixin** | add `RegularUserRequiredMixin` |
| `SearchProfileListView`, `KiezRadarView` (kiezauswahl) | [`apps/kiezradar/views.py`](../meinberlin/apps/kiezradar/views.py) | `LoginRequiredMixin` | → `RegularUserRequiredMixin` |
| allauth account pages (`/accounts/email/`, `/accounts/password/change/`, …) | `allauth.urls`, mounted in [`config/urls.py`](../meinberlin/config/urls.py) | `is_authenticated` | ⚠️ **Gap inherited from a+** (a+ mounts `allauth.urls` unguarded too). Guests can reach these. No single mixin point — needs per-view override or namespace-based middleware. See note below. |

**allauth gap (a+ parity issue):** a+ only guards its *own* `/account/` views with `RegularUserRequiredMixin`; it includes `allauth.urls` unguarded, so guests in a+ can reach `/accounts/email/` and `/accounts/password/change/`. meinBerlin mounts allauth identically ([`config/urls.py`](../meinberlin/config/urls.py) line 131), so it would inherit the gap. Password change is self-limiting (guests don't know their generated password), but email management is reachable. ⚠️ Decide whether to close it (override the allauth `account_email`/password views with a regular-user guard, or add lightweight middleware keyed on the `account_*` URL names) — and, if fixing, whether to also propose the fix upstream in a+.

**Must ALLOW guests — verify, no change expected:** comments, ratings, likes, ideas, mapideas, topicprio, maptopicprio, budgeting, polls APIs — all gate via `is_context_member`/module predicates and are covered by item 3.

### 6. Notification emails

- Guests have `NotificationSettings` (defaults on), so they pass `_exclude_notifications_disabled` and would be **queued for real emails** (e.g. `NotifyCreatorEmail` when someone replies to a guest's post; `NotifyCreatorOrContactOnModeratorFeedback`) to `guest-{uuid}@guest.invalid`.
- Add a `_exclude_guest_users(receivers)` helper (mirror the existing `_exclude_*` helpers in [`apps/notifications/emails.py`](../meinberlin/apps/notifications/emails.py) — handle querysets, user lists, and raw email strings).
- **Apply it centrally**, not per-class. a4's `EmailBase.dispatch` reads `self.get_receivers()` once before sending; override `dispatch` (or wrap receiver consumption) in meinBerlin's base `Email` ([`apps/contrib/emails.py`](../meinberlin/apps/contrib/emails.py)) so it catches all ~8 notification classes plus any a4/future ones. Applying it inside each `get_receivers` is easy to miss.
- In-app `Notification` rows are still created for guests (desired) — no change; they surface after convert.

### 7. Guest username display

**Decided: friendly `Guest####` names** via `generate_numbered_username` (e.g. `Guest4810`) — see settings in item 2. Satisfies `USERNAME_REGEX` and length. Convert lets the user pick a real username. Collisions with existing usernames are handled by the creation retry loop.

### Guest lifecycle & data retention (ties to items 2 & 6)

- **One-time, no re-login (confirmed):** guests are created on demand and logged in via session; they never re-authenticate. The fork gives guests a random UUID password + `guest+…@liqd.net` email, and `GuestBackend` authenticates by username without a password — but nothing calls it after creation, and guests never learn their credentials, so the normal login form cannot re-authenticate them. **Requirement: do not add any endpoint that invokes `GuestBackend` post-creation** (the library ships none).
- **`SESSION_EXPIRE_AT_BROWSER_CLOSE = True`** ([`settings/base.py`](../meinberlin/config/settings/base.py)): the guest session dies on browser close. Combined with no re-login, **convert must be offered within the same session** — after the browser closes the guest can never convert or return.
- **Retention — DECIDED: contribution-aware daily cleanup.** We do **not** use the library's stock `delete_expired_users` (it deletes by age alone and would cascade-delete contributions via `UserGeneratedContentModel.creator = on_delete=CASCADE`). Instead, meinBerlin ships a custom management command [`delete_expired_guests`](../meinberlin/apps/users/management/commands/delete_expired_guests.py):
  - Targets `Guest` rows older than **14 days** (`--days`, default 14) — converted users are already excluded because their `Guest` row is deleted on `email_confirmed`.
  - Deletes only guests with **no participation content** (no `Item`/idea, `Comment`, poll `Vote`/`Answer`, or non-zero `Rating` — mirrors `has_no_non_initiator_contributions`). Guests **with** contributions are kept, so nothing meaningful is ever cascade-deleted.
  - Supports `--dry-run`.
  - **Scheduling:** run daily from the external admin repo's `daily_manage_task` list (alongside `clearsessions`) — **no `CELERY_BEAT_SCHEDULE` entry in meinBerlin.**
