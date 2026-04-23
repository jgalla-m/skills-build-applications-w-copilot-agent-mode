from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the database with sample data for users, teams, activities, workouts, and leaderboard.'

    def handle(self, *args, **kwargs):
        # Create Users
        user1, _ = User.objects.get_or_create(username='alice', email='alice@example.com')
        user2, _ = User.objects.get_or_create(username='bob', email='bob@example.com')
        user3, _ = User.objects.get_or_create(username='carol', email='carol@example.com')

        # Create Teams
        team1, _ = Team.objects.get_or_create(name='Team Alpha')
        team2, _ = Team.objects.get_or_create(name='Team Beta')
        team1.members.set([user1, user2])
        team2.members.set([user3])

        # Create Workouts
        workout1, _ = Workout.objects.get_or_create(name='Morning Cardio', description='A quick morning cardio routine.')
        workout2, _ = Workout.objects.get_or_create(name='Strength Training', description='Full body strength workout.')
        workout1.suggested_for.set([user1, user3])
        workout2.suggested_for.set([user2])

        # Create Activities
        Activity.objects.get_or_create(user=user1, activity_type='Running', duration=30, calories_burned=300, date=timezone.now().date())
        Activity.objects.get_or_create(user=user2, activity_type='Cycling', duration=45, calories_burned=400, date=timezone.now().date())
        Activity.objects.get_or_create(user=user3, activity_type='Swimming', duration=60, calories_burned=500, date=timezone.now().date())

        # Create Leaderboard
        Leaderboard.objects.get_or_create(user=user1, total_points=120, rank=1)
        Leaderboard.objects.get_or_create(user=user2, total_points=100, rank=2)
        Leaderboard.objects.get_or_create(user=user3, total_points=80, rank=3)

        self.stdout.write(self.style.SUCCESS('Database populated with sample data.'))
