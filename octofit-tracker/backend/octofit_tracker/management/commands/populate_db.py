from __future__ import annotations

import random
from datetime import timedelta

from django.core.management.base import BaseCommand

from django.db import transaction
from django.utils import timezone
from octofit_tracker.models import User, Activity, Workout, Team, Leaderboard


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

    @transaction.atomic
    def handle(self, *args, **options):
        random.seed(42)

        # Clean up old data
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Team.objects.all().delete()
        User.objects.all().delete()

        # Create users
        users = []
        for i in range(4):
            username = ["superman", "batman", "ironman", "spiderman"][i]
            email = f"{username}@example.com"
            u = User.objects.create(username=username, email=email)
            users.append(u)

        # Create teams
        team_dc = Team.objects.create(name="Team DC")
        team_marvel = Team.objects.create(name="Team Marvel")
        team_dc.members.add(users[0], users[1])
        team_marvel.members.add(users[2], users[3])

        # Create workouts
        workout1 = Workout.objects.create(name="Morning Cardio", description="A quick morning cardio routine.")
        workout2 = Workout.objects.create(name="Strength Training", description="Full body strength workout.")
        workout1.suggested_for.add(users[0], users[2])
        workout2.suggested_for.add(users[1], users[3])

        # Create activities
        Activity.objects.create(user=users[0], activity_type="Flying", duration=60, calories_burned=500, date=timezone.now().date())
        Activity.objects.create(user=users[1], activity_type="Martial Arts", duration=45, calories_burned=400, date=timezone.now().date())
        Activity.objects.create(user=users[2], activity_type="Engineering", duration=90, calories_burned=350, date=timezone.now().date())
        Activity.objects.create(user=users[3], activity_type="Web Swinging", duration=30, calories_burned=250, date=timezone.now().date())

        # Create leaderboard
        Leaderboard.objects.create(user=users[0], total_points=150, rank=1)
        Leaderboard.objects.create(user=users[1], total_points=120, rank=2)
        Leaderboard.objects.create(user=users[2], total_points=110, rank=3)
        Leaderboard.objects.create(user=users[3], total_points=100, rank=4)

        self.stdout.write(self.style.SUCCESS("Database populated with superhero sample data."))
