from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
import random


class Command(BaseCommand):
    help = "Populate the database with sample data."

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating sample data...")

        # Clear existing data
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        Activity.objects.all().delete()
        Team.objects.all().delete()
        User.objects.all().delete()

        # Create Users
        users = []
        for i in range(1, 6):
            user = User.objects.create(
                username=f"user{i}",
                email=f"user{i}@example.com"
            )
            users.append(user)

        # Create Teams
        team1 = Team.objects.create(name="Team Alpha")
        team2 = Team.objects.create(name="Team Beta")

        # Assign users to teams
        for user in users[:3]:
            team1.members.add(user)

        for user in users[3:]:
            team2.members.add(user)

        # Create Activities
        activity_types = ["Running", "Cycling", "Swimming", "Yoga"]

        activities = []
        for name in activity_types:
            activity = Activity.objects.create(name=name)
            activities.append(activity)

        # Create Workouts
        workouts = []
        for user in users:
            for _ in range(3):
                activity = random.choice(activities)
                duration = random.randint(20, 90)

                workout = Workout.objects.create(
                    user=user,
                    activity=activity,
                    duration=duration,
                    date=timezone.now()
                )
                workouts.append(workout)

        # Create Leaderboard (sum durations per user)
        for user in users:
            total_score = sum(
                w.duration for w in workouts if w.user == user
            )

            Leaderboard.objects.create(
                user=user,
                score=total_score
            )

        self.stdout.write(self.style.SUCCESS("Database populated successfully!"))