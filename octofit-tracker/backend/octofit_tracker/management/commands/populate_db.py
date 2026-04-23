"""
Populate the local database with sample data for the GitHub Skills exercise.

Common usage:
  python populate_db.py

This script assumes:
- You have a Flask app factory create_app()
- SQLAlchemy db object
- Models such as User, Post, Comment (adjust as needed)
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta

# --- Update these imports to match your repository layout ---
# Typical layouts:
#   from app import create_app, db
#   from app.models import User, Post, Comment
# or
#   from src.app import create_app, db
#   from src.models import User, Post, Comment

from app import create_app, db  # noqa: E402
from app.models import User, Post, Comment  # noqa: E402


FIRST_NAMES = [
    "Avery", "Jordan", "Riley", "Casey", "Morgan", "Taylor", "Quinn", "Jamie",
    "Reese", "Skyler", "Rowan", "Parker",
]
LAST_NAMES = [
    "Nguyen", "Patel", "Garcia", "Johnson", "Kim", "Brown", "Martinez", "Lee",
    "Davis", "Lopez", "Wilson", "Anderson",
]
TOPICS = [
    "Copilot", "Flask", "SQLAlchemy", "APIs", "Testing", "Refactoring",
    "Python", "GitHub Actions", "Databases", "Prompting",
]
SENTENCES = [
    "Today I learned something new.",
    "This was easier than I expected.",
    "Here’s a small tip that saved me time.",
    "I hit an error, but the fix was straightforward.",
    "I’m documenting this for future me.",
    "This is a great place to start experimenting.",
    "I’m keeping this example intentionally simple.",
]


def random_name() -> tuple[str, str]:
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)


def random_email(first: str, last: str, n: int) -> str:
    return f"{first.lower()}.{last.lower()}{n}@example.com"


def random_title() -> str:
    return f"{random.choice(TOPICS)}: {random.choice(['notes', 'quickstart', 'walkthrough', 'tips', 'pitfalls'])}"


def random_body(paragraphs: int = 2) -> str:
    out = []
    for _ in range(paragraphs):
        lines = random.sample(SENTENCES, k=min(3, len(SENTENCES)))
        out.append(" ".join(lines))
    return "\n\n".join(out)


def reset_db() -> None:
    """Drop and recreate all tables (dev only)."""
    db.drop_all()
    db.create_all()


def seed_users(count: int = 8) -> list[User]:
    users: list[User] = []
    for i in range(1, count + 1):
        first, last = random_name()
        u = User(
            name=f"{first} {last}",
            email=random_email(first, last, i),
        )
        users.append(u)
        db.session.add(u)
    db.session.commit()
    return users


def seed_posts(users: list[User], posts_per_user: int = 3) -> list[Post]:
    posts: list[Post] = []
    now = datetime.utcnow()

    for u in users:
        for idx in range(posts_per_user):
            created_at = now - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
            p = Post(
                title=random_title(),
                body=random_body(paragraphs=random.randint(1, 3)),
                user_id=u.id,
                created_at=created_at,
            )
            posts.append(p)
            db.session.add(p)

    db.session.commit()
    return posts


def seed_comments(users: list[User], posts: list[Post], count: int = 20) -> list[Comment]:
    comments: list[Comment] = []
    now = datetime.utcnow()

    for _ in range(count):
        u = random.choice(users)
        p = random.choice(posts)
        created_at = now - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        c = Comment(
            body=random_body(paragraphs=1),
            user_id=u.id,
            post_id=p.id,
            created_at=created_at,
        )
        comments.append(c)
        db.session.add(c)

    db.session.commit()
    return comments


def main() -> None:
    random.seed(42)

    app = create_app()
    with app.app_context():
        print("Resetting database...")
        reset_db()

        print("Seeding users...")
        users = seed_users(count=8)

        print("Seeding posts...")
        posts = seed_posts(users, posts_per_user=3)

        print("Seeding comments...")
        seed_comments(users, posts, count=24)

        print("Done. Database populated successfully.")


if __name__ == "__main__":
    main()