# Guest users: meinBerlin vs adhocracy-plus

Comparison of guest-user implementations. a+ includes **uncommitted local changes** (auth hardening, notification email skip, allauth guards) — noted as **a+ (working tree)** vs **a+ HEAD** where they differ.

Both pin `django-guest-user@8fa934f` (branch `jp-26-07-change-backend-for-auth`).

---

## At a glance

| Feature | a+ | mB | Notes |
| --- | --- | --- | --- |
| `GuestBackend` omitted | Yes | Yes | Required; `W001` warns if registered |
| Guest create login | `maybe_create_guest_user` (fork `@8fa934f`) | Same | Uses `ModelBackend` login in fork |
| Guest name format | UUID (`generate_uuid_username` in config*) | `Guest#####` (`GUEST_USER_NAME_SUFFIX_DIGITS=5`) | *see [config caveat](#config-caveat) |
| `USERNAME_FIELD` | `username` | `email` | Biggest structural difference |
| `PASSWORD_FIELD` | `username` | `username` | Same |
| allauth account page guards | a+ (working tree) | Yes | `regular_user_required` on email/password views |
| Notification emails to guests | Skip in `NotificationService` (working tree) | Skip in base `Email.dispatch` | mB blocks all outbound mail |
| Follow API block for guests | No | Yes | mB `FollowViewSet(IsRegularUser)` |
| Kiezradar / search profiles | N/A | Gated (rules + React) | mB-only |
| `delete_expired_guests` command | Yes (local, uncommitted) | Yes | Same: 14d, no contributions |
| Guest account deletion | Yes | No | a+-only |
| Guest org agreements | Yes | No | mB uses site-wide terms only |
| Anonymous guest CTA on project | Yes (dismissible JS) | No | mB alerts logged-in guests only |
| `is_regular_user` / `IsRegularUser` | Inline checks only | Dedicated files | mB formalizes primitives |

---

## File mapping

| a+ | mB | Relationship |
| --- | --- | --- |
| `adhocracy-plus/config/settings/base.py` | `meinberlin/config/settings/base.py` | Adapted |
| `adhocracy-plus/config/urls.py` | `meinberlin/config/urls.py` | Adapted |
| `apps/users/models.py` | `meinberlin/apps/users/models.py` | Adapted |
| `apps/users/views.py` | `meinberlin/apps/users/views.py` | Adapted (+ mB `CustomLoginView`) |
| `apps/users/forms.py` | `meinberlin/apps/users/forms.py` | Adapted |
| `apps/users/signals.py` | `meinberlin/apps/users/signals.py` | Adapted |
| `apps/account/views.py` | `meinberlin/apps/account/views.py` | Adapted |
| `apps/account/urls.py` | `meinberlin/apps/account/urls.py` | a+ has extra guest routes |
| `apps/projects/rules.py` | `meinberlin/apps/projects/rules.py` | Adapted |
| `apps/notifications/services.py` | `meinberlin/apps/contrib/emails.py` | Different layer |
| `apps/notifications/views.py` | `meinberlin/apps/account/views.py`, `notifications/api.py` | Different architecture |
| — | `meinberlin/apps/users/predicates.py` | mB-only |
| — | `meinberlin/apps/users/permissions.py` | mB-only |
| — | `meinberlin/apps/users/management/commands/delete_expired_guests.py` | Ported to a+ `apps/users/management/commands/` |
| — | `meinberlin/apps/projects/api.py` (`FollowViewSet`) | mB-only |
| `apps/users/templatetags/signup_flow.py` | — | a+-only (`guest_url`) |
| `apps/projects/assets/js/guest_project_alert.js` | — | a+-only |
| — | `meinberlin/react/plans/SaveSearchProfile.jsx` (+ chain) | mB-only |

---

## Side-by-side: core guest flow

### Guest creation (`GuestCreateView`)

**Shared (mB + a+):** `maybe_create_guest_user(request)` in `GuestCreateView`; no `GuestBackend` in settings.

### Settings

| Setting | a+ | mB |
| --- | --- | --- |
| `AUTHENTICATION_BACKENDS` | No `GuestBackend` (working tree) | No `GuestBackend` |
| `SILENCED_SYSTEM_CHECKS` | — | — | Not needed after `@8fa934f` |
| `A4_ENABLE_GUEST_USERS` | `True` | `True` |
| Name generator (intended) | `generate_uuid_username` | `generate_numbered_username` |
| `GUEST_USER_NAME_SUFFIX_DIGITS` | — | `5` |
| `GUEST_USER_REQUIRED_ANON_URL` | `/accounts/guests/login` | `/accounts/guests/login/` |

### User model

| | a+ | mB |
| --- | --- | --- |
| `USERNAME_FIELD` | `"username"` | `"email"` |
| `REQUIRED_FIELDS` | `["email"]` | `["username"]` |
| `PASSWORD_FIELD` | `"username"` | `"username"` |
| `email` unique | No | Yes |

**What `USERNAME_FIELD = "email"` means for mB:** regular users log in with email; guests still get both `username` (`Guest04810`) and synthetic `email` (`guest+Guest04810@liqd.net`). Login form label says "username or email" because `ACCOUNT_LOGIN_METHODS = {"username", "email"}` — unrelated to guest flow.

### Guest convert

Both: `GuestConvertView` → `complete_signup` → mandatory email confirm → delete `Guest` row on `email_confirmed`.

| | a+ | mB |
| --- | --- | --- |
| Convert form base | `DefaultSignupForm` | `TermsSignupForm` |
| Post-convert prefs | `get_newsletters` on user | `NotificationSettings` via `update_email_settings()` |
| Captcha on convert | No | No |
| Welcome email on confirm | No | Yes |

### URLs (guest + allauth)

**Shared (a+ working tree, mB committed):**

```
accounts/guests/login/          → GuestCreateView
accounts/email/                 → regular_user_required(EmailView)
accounts/password/change/       → regular_user_required(PasswordChangeView)
accounts/password/set/          → regular_user_required(PasswordSetView)
accounts/                       → include(allauth.urls)
```

**mB-only:** `accounts/login/` → `CustomLoginView` (conditional guest CTA, referer `next`).

**a+-only account routes:** `/account/guest/account_deletion/`, `/account/guest/agreements/`.

---

## Where they diverge (product / scope)

### mB-only

- **`is_regular_user` / `IsRegularUser`** — shared predicate + DRF permission
- **API hard-blocks** — follows, notifications, kiezradar
- **Central email exclusion** — `contrib/emails.Email.dispatch`
- **React** — `isGuestUser` hides `SaveSearchProfile` on plans map
- **Kiezradar** — `RegularUserRequiredMixin` on views + rules
- **Logged-in guest alert** on project detail (not anonymous CTA)
- **Broader `RegularUserRequiredMixin`** — followed projects, kiezradar, etc.

### a+-only (account UX)

a+ does **not** mean guests have a separate app — it means guests who reach `/account/` get a **dedicated sidebar** inside the shared account dashboard layout (`account_dashboard.html`): Convert Account, User Agreements, Delete account. Regular users see the full sidebar (profile, password, notifications, email, etc.).

mB blocks guests from `/account/` views entirely (`RegularUserRequiredMixin`) and points them to convert via hamburger nav ("Create an account") instead.

| | a+ | mB |
| --- | --- | --- |
| Guest can open `/account/` | Yes — guest sidebar | No — redirected/blocked |
| Convert page | `/account/guest/convert/` | `/account/guest/convert/` |
| Guest delete account | Yes (`GuestAccountDeletionForm`, no password) | No |
| Per-org guest agreements | Yes (`/account/guest/agreements/`) | No (site-wide terms only) |

**Also a+-only (outside account):** anonymous guest CTA on project detail (`guest_project_alert.js`), `signup_flow.guest_url` templatetag, user indicator "Guest" label in header.

### Shared operational cleanup

Both codebases: `delete_expired_guests` — guests older than 14 days with no participation content (ideas, comments, votes, answers, non-neutral ratings). `--dry-run` supported. Intended for daily cron beside `clearsessions`.

### Same intent, different surface

| Concern | a+ | mB |
| --- | --- | --- |
| Hide notifications for guests | Header bell + user dashboard mixin | `navigation_primary.html` + API |
| Hide follow widget | `project_detail_intro.html` | `hero.html` |
| Block guest emails | `NotificationService` (working tree) | All emails via base `Email` class |
| `guest_may_participate` | In `participate_in_project` rule | Same (different rule preconditions) |

---

## `projects/rules.py` — participate rule

Both append `& guest_may_participate` to the public participate branch.

- **a+:** `(is_public | is_org_member | is_project_member) & is_live & guest_may_participate`
- **mB:** `(is_public | is_project_member) & is_live & guest_may_participate` (no org-member branch; uses `is_prj_group_member` elsewhere)

---

## Tests

| | a+ (working tree) | mB |
| --- | --- | --- |
| Helper | `tests/helpers.py` — `GuestUserCreator` | `meinberlin/test/helpers.py` — same pattern |
| Auth security | `tests/users/test_guest_auth.py` (2) | Same + in `test_guest_users.py` |
| Notification email skip | `tests/notifications/test_guest_notifications.py` (2) | Overlap + welcome-email skip |
| Full suite | Thin / distributed | `tests/users/test_guest_users.py` (24 tests) |
| Cleanup command | — | 4 tests |

---

## a+ uncommitted diff (working tree)

```
 M adhocracy-plus/config/settings/base.py
 M adhocracy-plus/config/urls.py
 M apps/notifications/services.py
 M apps/notifications/views.py
 M apps/users/views.py
 M tests/helpers.py
?? tests/notifications/test_guest_notifications.py
?? tests/users/test_guest_auth.py
```

**a+ uncommitted diff** brings a+ in line with mB: fork pin `@8fa934f`, allauth guards, notification email skip, `delete_expired_guests`, security tests. **roots** unchanged (frozen on `@cfee4f0`).

---

## Config caveat

Both codebases have:

```python
GUEST_USER = {
    "NAME_GENERATOR": "...",
}
```

django-guest-user reads **flat** `GUEST_USER_*` settings, not this dict. Default generator is `generate_numbered_username` → `Guest####` unless `GUEST_USER_NAME_GENERATOR` is set. a+'s UUID config may never have been active in production; mB sets `GUEST_USER_NAME_SUFFIX_DIGITS = 5` explicitly.

---

## Related docs

- [`guest_user_port.md`](guest_user_port.md) — mB build plan
- [`guest_users_for_later.md`](guest_users_for_later.md) — deferred fork/config notes
- [`aplus_guest_notification_emails.md`](aplus_guest_notification_emails.md) — a+ email plan
