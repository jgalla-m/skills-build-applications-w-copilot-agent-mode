from __future__ import annotations

import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

# Update these imports to match your actual models module.
# Common patterns:
#   from octofit_tracker.models import Activity, Workout
#   from octofit_tracker.models import Activity, WorkoutLog
try:
    from octofit_tracker.models import Activity, WorkoutLog  # type: ignore
except Exception:  # pragma: no cover
    Activity = None  # type: ignore
    WorkoutLog = None  # type: ignore


FIRST_NAMES = ["Avery", "Jordan", "Riley", "Casey", "Morgan", "Taylor", "Quinn", "Jamie"]
LAST_NAMES = ["Nguyen", "Patel", "Garcia", "Johnson", "Kim", "Brown", "Martinez", "Lee"]

ACTIVITIES = [
    ("Run", "Cardio"),
    ("Walk", "Cardio"),
    ("Cycling", "Cardio"),
    ("Rowing", "Cardio"),
    ("Yoga", "Flexibility"),
    ("Strength Training", "Strength"),
]


def _rand_name() -> tuple[str, str]:
    return random.choice(FIRST_NAMES), random.choice(LAST_NAMES)


def _rand_email(first: str, last: str, n: int) -> str:
    return f"{first.lower()}.{last.lower()}{n}@example.com"


class Command(BaseCommand):
    help = "Populate the database with sample OctoFit Tracker data."

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=8, help="Number of sample users to create.")
        parser.add_argument("--logs", type=int, default=40, help="Number of workout logs to create.")
        parser.add_argument(
            "--create-superuser",
            action="store_true",
            help="Create a demo superuser (admin/admin12345) if it doesn't exist.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        random.seed(42)

        if Activity is None or WorkoutLog is None:
            raise RuntimeError(
                "Could not import Activity/WorkoutLog models. "
                "Update the imports in populate_db.py to match your project models."
            )

        User = get_user_model()

        users_count: int = options["users"]
        logs_count: int = options["logs"]
        create_superuser: bool = options["create_superuser"]

        if create_superuser:
            admin_username = "admin"
            admin_password = "admin12345"
            admin_email = "admin@example.com"

            admin, created = User.objects.get_or_create(
                username=admin_username,
                defaults={"email": admin_email},
            )
            if created or not admin.is_superuser:
                admin.is_staff = True
                admin.is_superuser = True
                admin.set_password(admin_password)
                admin.save()

            self.stdout.write(self.style.SUCCESS(f"Superuser ready: {admin_username}/{admin_password}"))

        # Create sample users
        users = []
        for i in range(1, users_count + 1):
            first, last = _rand_name()
            username = f"{first.lower()}{last.lower()}{i}"

            u, _ = User.objects.get_or_create(
                username=username,
                defaults={"email": _rand_email(first, last, i)},
            )
            # If your User model requires more fields, set them here.
            users.append(u)

        # Create activities
        activities = []
        for name, category in ACTIVITIES:
            # Adjust field names if your Activity model differs.
            a, _ = Activity.objects.get_or_create(
                name=name,
                defaults={"category": category},
            )
            activities.append(a)

        # Create workout logs
        now = timezone.now()
        created_logs = 0

        for _ in range(logs_count):
            user = random.choice(users)
            activity = random.choice(activities)

            minutes = random.choice([20, 30, 40, 45, 60])
            calories = minutes * random.randint(6, 12)
            performed_at = now - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))

            # Adjust field names if your WorkoutLog model differs.
            WorkoutLog.objects.create(
                user=user,
                activity=activity,
                duration_minutes=minutes,
                calories_burned=calories,
                performed_at=performed_at,
            )
            created_logs += 1

        self.stdout.write(self.style.SUCCESS(f"Created/ensured {len(users)} users"))
        self.stdout.write(self.style.SUCCESS(f"Created/ensured {len(activities)} activities"))
        self.stdout.write(self.style.SUCCESS(f"Created {created_logs} workout logs"))
        self.stdout.write(self.style.SUCCESS("Database populated successfully."))