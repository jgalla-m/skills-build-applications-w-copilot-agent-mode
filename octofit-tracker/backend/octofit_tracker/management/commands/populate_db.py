from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate the database with sample data for users, teams, activities, workouts, and leaderboard.'

    def handle(self, *args, **kwargs):
        # 🔥 Clean start (często wymagane przez testy)
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Team.objects.all().delete()
        User.objects.all().delete()

        # --------------------
        # USERS
        # --------------------
        user1 = User.objects.create(username='alice', email='alice@example.com')
        user2 = User.objects.create(username='bob', email='bob@example.com')
        user3 = User.objects.create(username='carol', email='carol@example.com')

        # --------------------
        # TEAMS
        # --------------------
        team1 = Team.objects.create(name='Team Alpha')
        team2 = Team.objects.create(name='Team Beta')

        team1.members.add(user1, user2)
        team2.members.add(user3)

        # --------------------
        # WORKOUTS
        # --------------------
        workout1 = Workout.objects.create(
            name='Morning Cardio',
            description='A quick morning cardio routine.'
        )
        workout2 = Workout.objects.create(
            name='Strength Training',
            description='Full body strength workout.'
        )

        workout1.suggested_for.add(user1, user3)
        workout2.suggested_for.add(user2)

        # --------------------
        # ACTIVITIES
        # --------------------
        Activity.objects.create(
            user=user1,
            activity_type='Running',
            duration=30,
            calories_burned=300,
            date=timezone.now().date()
        )

        Activity.objects.create(
            user=user2,
            activity_type='Cycling',
            duration=45,
            calories_burned=400,
            date=timezone.now().date()
        )

        Activity.objects.create(
            user=user3,
            activity_type='Swimming',
            duration=60,
            calories_burned=500,
            date=timezone.now().date()
        )

        # --------------------
        # LEADERBOARD
        # --------------------
        Leaderboard.objects.create(user=user1, total_points=120, rank=1)
        Leaderboard.objects.create(user=user2, total_points=100, rank=2)
        Leaderboard.objects.create(user=user3, total_points=80, rank=3)

        self.stdout.write(self.style.SUCCESS('Database populated with sample data.'))