"""One-off migration: rename the remaining placeholder users (bob/carol/
dave/erin/frank@example.com) to the real league members, in place.

Renames existing rows via UPDATE rather than delete+recreate, so it's safe
to run against a database with an already-created Auction — nomination
order and turn derivation reference user_id, not email/display_name, so
they're untouched by this. Safe to re-run — rows already renamed just
won't match any old email.
"""

from app.database import SessionLocal
from app.models import User

RENAMES = {
    "bob@example.com": ("Sean K", "demedici@gmail.com"),
    "carol@example.com": ("Andrew D", "adaniller@gmail.com"),
    "dave@example.com": ("Phil F", "lowellpf@gmail.com"),
    "erin@example.com": ("Liam T", "liamtoohey@gmail.com"),
    "frank@example.com": ("John R", "john.rackson@gmail.com"),
}


def run() -> None:
    db = SessionLocal()
    renamed = 0
    skipped = 0
    for old_email, (display_name, new_email) in RENAMES.items():
        user = db.query(User).filter(User.email == old_email).first()
        if user is None:
            print(f"  no user found for {old_email!r} — already renamed or never seeded")
            skipped += 1
            continue
        user.email = new_email
        user.display_name = display_name
        renamed += 1
    db.commit()
    print(f"renamed={renamed} skipped={skipped}")


if __name__ == "__main__":
    run()
