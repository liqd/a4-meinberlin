---
name: a+ guest notification emails
overview: Block outbound notification emails to guest users in adhocracy-plus while keeping in-app Notification row creation unchanged. After email confirm, users see in-app notification backlog; suppressed emails are not resent.
todos:
  - id: a-plus-email-filter
    content: Add is_guest_user skip for email channel in NotificationService._filter_recipients_by_preferences
    status: completed
  - id: a-plus-settings-mixin
    content: Add RegularUserRequiredMixin to NotificationSettingsView
    status: completed
  - id: a-plus-guest-notification-tests
    content: "Tests: guest gets Notification row + no email; after email confirm, backlog visible + new emails sent"
    status: completed
isProject: false
---

# a+ Guest notification email fix

## Context

adhocracy-plus already blocks **guest access** to the notifications UI:

- Header bell hidden (`header_notification_button.html` — `is_guest_user`)
- User dashboard / notifications page: `RegularUserRequiredMixin` on `UserDashboardBaseMixin` (`[apps/userdashboard/views.py](file:///Users/josh/projects/adhocracy-plus/apps/userdashboard/views.py)`)
- Guest account nav: Convert / Agreements / Delete only — no notifications link

**In-app `Notification` rows are already created** for guests via `[NotificationService.create_notifications](file:///Users/josh/projects/adhocracy-plus/apps/notifications/services.py)` — this is **correct** and should stay. After convert, the same `User` pk sees the backlog.

**Gap:** `NotificationService` does not filter guests from `email_recipients`. A guest who posts content can receive notification emails to `guest+{username}@liqd.net`.

meinBerlin port will implement the same split (rows yes, email/UI no while guest). This plan is the a+ counterpart — email blocking only.

## Changes

### 1. Block guest emails in NotificationService

File: `[apps/notifications/services.py](file:///Users/josh/projects/adhocracy-plus/apps/notifications/services.py)`

In `_filter_recipients_by_preferences`, skip guests when `channel == "email"`:

```python
from guest_user.functions import is_guest_user

# inside the recipient loop:
if channel == "email" and is_guest_user(recipient):
    continue
```

**Do not** filter guests from `in_app` channel — rows should still be created.

Alternative: filter `email_recipients` only in `_get_filtered_recipients` after preference filtering. Same effect.

### 2. Harden NotificationSettingsView (minor)

File: `[apps/notifications/views.py](file:///Users/josh/projects/adhocracy-plus/apps/notifications/views.py)`

`NotificationSettingsView` currently uses `LoginRequiredMixin` only. Add `RegularUserRequiredMixin` so guests cannot reach `/account/notification-settings/` by direct URL (nav already hides it).

### 3. Tests

Add to `tests/notifications/`:

- Guest posts content → interaction triggers notification → assert `Notification` row exists for guest
- Assert **no** notification email sent to guest address
- Convert guest → assert notification page accessible
- After convert → assert notification email sent for new events (per settings)

Reuse `GuestUserCreator` from `[tests/helpers.py](file:///Users/josh/projects/adhocracy-plus/tests/helpers.py)`.

## Out of scope

- Changing in-app notification creation logic
- Guest convert flow (already works)
- meinBerlin implementation (separate plan: port guest users to meinberlin)

## After convert — what users get

Convert is two steps: **convert form** → **email confirmation** (`Guest` row deleted on `email_confirmed` in `[apps/users/signals.py](file:///Users/josh/projects/adhocracy-plus/apps/users/signals.py)`). Until email is confirmed, `is_guest_user` is still true (no notifications UI, no emails).


|                               | During guest (+ pending confirm) | After email confirm                                                                                                                                                                    |
| ----------------------------- | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **In-app notifications page** | Blocked                          | **Yes — backlog visible.** Rows were created with `recipient=user` (same pk); `request.user.notifications` shows everything from the guest period.                                     |
| **Email backlog**             | Suppressed at send time          | **No.** Emails are sent when events fire, not queued. Skipped guest emails are **not** resent on convert. Only **new** events after confirm trigger emails per `NotificationSettings`. |


This is intentional: guests have no real inbox during the guest phase; in-app feed is the catch-up mechanism.

## Behaviour summary


|                            | While guest           | After convert + email confirm |
| -------------------------- | --------------------- | ----------------------------- |
| In-app `Notification` rows | Created               | Visible in user dashboard     |
| Notifications UI           | Blocked (existing)    | Open                          |
| Outbound emails            | **Blocked (this PR)** | Per `NotificationSettings`    |


