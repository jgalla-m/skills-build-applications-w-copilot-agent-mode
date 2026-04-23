from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
import random

from octofit_tracker.models import Team, Activity, Workout, Leaderboard

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with sample data for users, teams, activities, workouts, and leaderboard.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Cleaning old data...")

        # opcjonalnie: czyścimy dane (ważne w ćwiczeniu)
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Team.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write("Creating users...")

        users = []
        for i in range(5):
            user = User.objects.create_user(
                username=f"user{i}",
                email=f"user{i}@example.com",
                password="password123"
            )
            users.append(user)

        self.stdout.write("Creating teams...")

        team1 = Team.objects.create(name="Team Alpha")
        team2 = Team.objects.create(name="Team Beta")

        # przypisanie userów do teamów (jeśli model ma FK/M2M)
        for user in users[:3]:
            user.team = team1
            user.save()

        for user in users[3:]:
            user.team = team2
            user.save()

        self.stdout.write("Creating activities...")

        activities = [
            Activity.objects.create(name="Running"),
            Activity.objects.create(name="Cycling"),
            Activity.objects.create(name="Swimming"),
        ]

        self.stdout.write("Creating workouts...")

        workouts = []
        for user in users:
            for _ in range(3):
                workout = Workout.objects.create(
                    user=user,
                    activity=random.choice(activities),
                    duration=random.randint(10, 120),  # minuty
                    calories_burned=random.randint(100, 800),
                    date=timezone.now()
                )
                workouts.append(workout)

        self.stdout.write("Creating leaderboard...")

        for user in users:
            total_points = sum(
                w.calories_burned for w in workouts if w.user == user
            )

            Leaderboard.objects.create(
                user=user,
                points=total_points
            )

        self.stdout.write(self.style.SUCCESS("Database populated successfully!"))