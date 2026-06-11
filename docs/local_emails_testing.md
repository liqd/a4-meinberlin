# Sending E-mails via command

1. In `a4-meinberlin` activate `virtual env (venv)`.
2. Run `python manage.py send_test_emails [your email]`.
3. Check mailbox of the specified email.

File: meinberlin/apps/notifications/management/commands/send_test_emails.py

## Publish-results reminder (initiators)

Sends the real publish-results reminder to initiators of the project’s organisation who are involved in the project (recorded in the admin log / changelog; one e-mail per initiator), **only if** the project satisfies the **same eligibility rules** as the periodic `send_publish_results_reminders` task (published standard project, not archived, results field empty, online participation ended, delay and optional minimum end date satisfied, and no reminder sent before).

1. Run `venv/bin/python manage.py send_publish_results_reminder <project-slug>` (slug as in `/projekte/<slug>/`).
2. Or Django admin → Projects → action “Send publish-results reminder…” (skipped projects show warning messages with reasons).

File: meinberlin/apps/projects/management/commands/send_publish_results_reminder.py

# Sending E-mails via background tasks

1. In `a4-meinberlin` activate `virtual env (venv)`.
2. Run `make background`.
3. Go to project in your browser.
4. Take actions (comment, report etc.) to trigger emails.
5. Check mailbox of email that gets notified.

File: Makefile
