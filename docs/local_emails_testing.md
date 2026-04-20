# Sending E-mails via command

1. In `a4-meinberlin` activate `virtual env (venv)`.
2. Run `python manage.py send_test_emails [your email]`.
3. Check mailbox of the specified email.

File: meinberlin/apps/notifications/management/commands/send_test_emails.py

## Publish-results reminder (initiators)

Sends the real publish-results reminder to every initiator of the project’s organisation (one e-mail per initiator). Ignores phase dates and whether a reminder was already sent. Draft projects are refused unless you pass `--force`.

1. Run `venv/bin/python manage.py send_publish_results_reminder <project-slug>` (slug as in `/projekte/<slug>/`).
2. Optional: `python manage.py send_publish_results_reminder <project-slug> --force` if the project is still unpublished.
3. Or Django admin → Projects → actions (drafts skipped).

File: meinberlin/apps/projects/management/commands/send_publish_results_reminder.py

# Sending E-mails via background tasks

1. In `a4-meinberlin` activate `virtual env (venv)`.
2. Run `make background`.
3. Go to project in your browser.
4. Take actions (comment, report etc.) to trigger emails.
5. Check mailbox of email that gets notified.

File: Makefile
