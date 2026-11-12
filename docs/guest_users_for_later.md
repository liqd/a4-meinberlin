# Guest users — for-later notes

Status snapshot after the meinBerlin port, adhocracy-plus follow-up, and fork security release.

## Security model (current)

Pin: **`django-guest-user@8fa934f`** (branch `jp-26-07-change-backend-for-auth`).

`maybe_create_guest_user` logs guests in via `GUEST_USER_LOGIN_BACKEND` (`ModelBackend`). **`GuestBackend` must not** be in `AUTHENTICATION_BACKENDS`. System check `guest_user.W001` warns if it is.

| Codebase | Fork pin | Notification email block | allauth account pages guarded |
| --- | --- | --- | --- |
| meinBerlin | `@8fa934f` | Done (central `Email.dispatch`) | Done |
| adhocracy-plus | `@8fa934f` (local, uncommitted) | Done | Done |
| roots | `@cfee4f0` (frozen) | N/A | N/A |

**roots:** dev frozen — keep old pin and `GuestBackend` until roots is unfrozen.

## meinBerlin settings

- `GUEST_USER_NAME_SUFFIX_DIGITS = 5` — ~99k name pool (`Guest00001`–`Guest99999`).
- Use flat `GUEST_USER_*` settings (the `GUEST_USER = {...}` dict is not read by the library).
- No `SILENCED_SYSTEM_CHECKS` for guest_user.

## adhocracy-plus changes (local, uncommitted)

| Area | Change |
| --- | --- |
| Fork pin | `@8fa934f`; `GuestCreateView` → `maybe_create_guest_user` |
| Notification emails | Skip guests in `NotificationService` email channel |
| Notification settings | `RegularUserRequiredMixin` on `NotificationSettingsView` |
| allauth gap | `regular_user_required` on email/password views |
| Guest cleanup | `delete_expired_guests` + tests |

Still to do: push fork branch, commit a+ changes, open PR.

## Fork (`liqd/django-guest-user@8fa934f`)

See fork `CHANGELOG.md`. Summary:

- `maybe_create_guest_user` → `create_guest_user` + `login(ModelBackend)`
- `GuestBackend.authenticate()` disabled
- `guest_user.W001` warns when `GuestBackend` **is** registered
- `create_guest_user` IntegrityError + explicit-username fixes

## Related docs

- [`guest_user_port.md`](guest_user_port.md) — meinBerlin build plan
- [`guest_users_mb_vs_aplus.md`](guest_users_mb_vs_aplus.md) — comparison
- [`aplus_guest_notification_emails.md`](aplus_guest_notification_emails.md) — a+ email plan
