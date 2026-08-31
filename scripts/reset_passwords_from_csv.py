#!/usr/bin/env python
"""Bulk password reset for users listed in a CSV file.

Reads a CSV file, matches each row against user accounts and either
blocks password login or sends the standard password-reset email.

Examples:
    # See what would happen, without changing anything
    python scripts/reset_passwords_from_csv.py --csv users.csv --dry-run

    # Disable passwords (users can no longer log in with a password)
    python scripts/reset_passwords_from_csv.py --csv users.csv

    # Send the standard "reset password" email with a reset link
    python scripts/reset_passwords_from_csv.py --csv users.csv --send-email

    # Disable the password AND send the reset link (recommended):
    # the link lets the user pick a new password and re-enables login
    python scripts/reset_passwords_from_csv.py --csv users.csv \
        --disable-passwords --send-email

    # Skip the confirmation prompt (for use in automation)
    python scripts/reset_passwords_from_csv.py --csv users.csv --yes

    # Results are appended to a timestamped CSV log, one row per action:
    # password_reset_results_20260831_143022.csv

CSV format (any columns are fine; pick the key column with --email-col
or --username-col):

    #,email,account_created,last_login
    1,sample@email.com,2017-10-12 14:00:11.848400,2017-10-12 14:00:27.181790
"""

import argparse
import csv
import getpass
import os
import sys
from datetime import datetime

# Make the project root importable when the script is run from anywhere.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meinberlin.config.settings")

# Django and project imports must follow django.setup() (standalone script).
import django  # noqa: E402

django.setup()

from allauth.account.forms import ResetPasswordForm  # noqa: E402
from allauth.core import context as allauth_context  # noqa: E402
from django.conf import settings  # noqa: E402
from django.contrib.sites.models import Site  # noqa: E402
from django.db import transaction  # noqa: E402
from django.db.models.functions import Lower  # noqa: E402
from django.test import RequestFactory  # noqa: E402
from django.utils import timezone  # noqa: E402

from meinberlin.apps.users.models import User  # noqa: E402

EXIT_OK = 0
EXIT_ERROR = 1

DESCRIPTION = __doc__.splitlines()[0]
EPILOG = "\n".join(__doc__.splitlines()[1:])


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--csv",
        default="users.csv",
        help="path to the CSV file (default: users.csv)",
    )
    parser.add_argument(
        "--email-col",
        default="email",
        help="column holding the e-mail address (default: email)",
    )
    parser.add_argument(
        "--username-col",
        default="username",
        help=(
            "column holding the username; used only when the email "
            "column is not present (default: username)"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="only show what would happen, do not change anything",
    )
    parser.add_argument(
        "--send-email",
        action="store_true",
        help="send the standard password-reset email with a reset link",
    )
    parser.add_argument(
        "--disable-passwords",
        action="store_true",
        help="set an unusable password (blocks password login)",
    )
    parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="do not ask for confirmation",
    )
    parser.add_argument(
        "--log-file",
        default=None,
        help=(
            "path of the CSV results log; defaults to "
            "password_reset_results_<timestamp>.csv in the current directory"
        ),
    )
    return parser.parse_args(argv)


def read_csv_keys(csv_path, email_col, username_col):
    """Return (mode, [(line_number, key), ...]) for the rows in the CSV."""
    try:
        with open(csv_path, newline="", encoding="utf-8-sig") as fh:
            rows = list(csv.DictReader(fh))
    except FileNotFoundError:
        print("error: CSV file not found: %s" % csv_path)
        sys.exit(EXIT_ERROR)

    if not rows:
        print("error: no data rows found in %s" % csv_path)
        sys.exit(EXIT_ERROR)

    fieldnames = set()
    for row in rows:
        fieldnames.update(row.keys())

    if email_col in fieldnames:
        mode = "email"
        key_col = email_col
    elif username_col in fieldnames:
        mode = "username"
        key_col = username_col
    else:
        available = ", ".join(sorted(fieldnames))
        print(
            "error: neither column %r nor %r found in CSV; "
            "available columns: %s" % (email_col, username_col, available)
        )
        sys.exit(EXIT_ERROR)

    # First data row is CSV line 2 (line 1 is the header row).
    keys = []
    for line_no, row in enumerate(rows, start=2):
        key = (row.get(key_col) or "").strip()
        if key:
            keys.append((line_no, key))

    if not keys:
        print("error: no non-empty values in column %r" % key_col)
        sys.exit(EXIT_ERROR)

    return mode, keys


def find_users(mode, keys):
    """Return a dict mapping normalized CSV keys to User instances."""
    if mode == "email":
        normalized = [key.lower() for (_, key) in keys]
        queryset = (
            User.objects.annotate(_key_lower=Lower("email"))
            .filter(_key_lower__in=normalized)
            .distinct()
        )
        return {user.email.lower(): user for user in queryset}

    usernames = [key for (_, key) in keys]
    queryset = User.objects.filter(username__in=usernames).distinct()
    return {user.username: user for user in queryset}


def group_keys(mode, keys, users_by_key):
    """Return (matches, missing, duplicate_count) for the CSV rows."""
    matches = []
    missing = []
    duplicates = 0
    seen = set()
    for line_no, key in keys:
        lookup = key.lower() if mode == "email" else key
        user = users_by_key.get(lookup)
        if user is None:
            missing.append((line_no, key))
        elif lookup in seen:
            duplicates += 1
        else:
            seen.add(lookup)
            matches.append((line_no, key, user))
    return matches, missing, duplicates


def build_request():
    """Build a fake request pointing at the configured site.

    allauth builds the reset link from the request, so the link must
    carry the site's real domain instead of the 'testserver' default.
    """
    request = RequestFactory().get("/")
    try:
        site = Site.objects.get_current()
    except Site.DoesNotExist:
        print(
            "warning: no Site row for SITE_ID=%s; "
            "reset links will point at '%s'"
            % (getattr(settings, "SITE_ID", None), request.get_host())
        )
        return request
    request.site = site
    request.META["SERVER_NAME"] = site.domain
    return request


def send_reset_email(user, request):
    """Send the standard reset email for one user.

    Uses the same allauth form as the website, so behaviour (e.g. only
    active users with a verified e-mail address) matches the site.
    """
    with allauth_context.request_context(request):
        form = ResetPasswordForm({"email": user.email})
        if not form.is_valid():
            return "error: %s" % form.errors.as_text()
        if not form.users:
            return "skipped: no active account with a verified e-mail address"
        form.save(request)
    return "reset e-mail sent"


def disable_password(user):
    user.set_unusable_password()
    user.save(update_fields=["password"])


def confirm(action_desc, count):
    """Ask for confirmation; return True when it is safe to proceed."""
    try:
        answer = input("Really %s for %d user(s)? (yes/no): " % (action_desc, count))
    except EOFError:
        print("")
        print("error: no confirmation given, use --yes to skip the prompt")
        return False
    if answer.strip().lower() != "yes":
        print("cancelled")
        return False
    return True


def make_log_path(log_file):
    """Return the results log path (timestamped by default)."""
    if log_file:
        return log_file
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return "password_reset_results_%s.csv" % stamp


def open_result_log(path):
    """Open the results log, writing a header row for new files."""
    is_new = not os.path.exists(path)
    try:
        fh = open(path, "a", newline="", encoding="utf-8")
    except OSError:
        print("error: cannot write results log: %s" % path)
        sys.exit(EXIT_ERROR)
    writer = csv.writer(fh)
    if is_new:
        writer.writerow(
            [
                "processed_at",
                "operator",
                "email",
                "username",
                "action",
                "result",
                "detail",
            ]
        )
    return fh, writer


def log_action(writer, user, action, result, detail=""):
    """Append one row to the results log (user may be None for summaries)."""
    writer.writerow(
        [
            timezone.now().isoformat(timespec="seconds"),
            getpass.getuser(),
            user.email if user else "",
            user.username if user else "",
            action,
            result,
            detail,
        ]
    )


def process_users(matches, args, request, writer):
    """Apply the requested actions to all matched users."""
    disabled = sent = skipped = failed = 0
    with transaction.atomic():
        for _, _, user in matches:
            parts = []
            if args.disable_passwords:
                disable_password(user)
                disabled += 1
                parts.append("password disabled")
                log_action(writer, user, "disable_password", "disabled")
            if args.send_email:
                result = send_reset_email(user, request)
                if result.startswith("error:"):
                    failed += 1
                    log_action(writer, user, "send_reset_email", "error", result)
                elif result.startswith("skipped:"):
                    skipped += 1
                    log_action(writer, user, "send_reset_email", "skipped", result)
                else:
                    sent += 1
                    log_action(writer, user, "send_reset_email", "sent")
                parts.append(result)
            print("  %s <%s>: %s" % (user.username, user.email, ", ".join(parts)))
    return disabled, sent, skipped, failed


def run_actions(matches, args, log_path):
    """Run the requested actions and return (disabled, sent, skipped, failed)."""
    log_fh, writer = open_result_log(log_path)
    request = build_request() if args.send_email else None
    try:
        disabled, sent, skipped, failed = process_users(matches, args, request, writer)
        log_action(
            writer,
            None,
            "summary",
            "done",
            "%d password(s) disabled, %d e-mail(s) sent, "
            "%d skipped, %d failed" % (disabled, sent, skipped, failed),
        )
    finally:
        log_fh.close()
    return disabled, sent, skipped, failed


def main():
    args = parse_args()

    # Default action mirrors the original script: block password login.
    if not args.send_email and not args.disable_passwords:
        args.disable_passwords = True

    actions = []
    if args.disable_passwords:
        actions.append("set an unusable password")
    if args.send_email:
        actions.append("send a password-reset e-mail")
    action_desc = " and ".join(actions)

    mode, keys = read_csv_keys(args.csv, args.email_col, args.username_col)
    users_by_key = find_users(mode, keys)
    matches, missing, duplicates = group_keys(mode, keys, users_by_key)

    if missing:
        shown = ", ".join(key for (_, key) in missing[:10])
        more = " ..." if len(missing) > 10 else ""
        print("warning: %d row(s) match no user: %s%s" % (len(missing), shown, more))
    if duplicates:
        print("note: %d duplicate row(s) ignored" % duplicates)

    if not matches:
        print("error: no matching users found, nothing to do")
        sys.exit(EXIT_ERROR)

    print("")
    print("%d user(s) to process:" % len(matches))
    for _, _, user in matches:
        print("  - %s <%s>" % (user.username, user.email))

    if args.dry_run:
        print("")
        print("dry run: would %s for %d user(s)" % (action_desc, len(matches)))
        print("no changes made, no results log written")
        sys.exit(EXIT_OK)

    if not args.yes and not confirm(action_desc, len(matches)):
        sys.exit(EXIT_ERROR)

    log_path = make_log_path(args.log_file)
    disabled, sent, skipped, failed = run_actions(matches, args, log_path)

    print("")
    print(
        "done: %d password(s) disabled, %d e-mail(s) sent, "
        "%d skipped, %d failed" % (disabled, sent, skipped, failed)
    )
    print("results logged to %s" % log_path)
    sys.exit(EXIT_ERROR if failed else EXIT_OK)


if __name__ == "__main__":
    main()
