
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from django.db import transaction, IntegrityError


class Command(BaseCommand):
    help = 'Populate the database with sample data for users, teams, activities, workouts, and leaderboard.'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                self.stdout.write('Deleting old data...')
                Leaderboard.objects.all().delete()
                Activity.objects.all().delete()
                Workout.objects.all().delete()
                Team.objects.all().delete()
                User.objects.all().delete()

                self.stdout.write('Creating users...')
                user1 = User(username='superman', email='superman@dc.com')
                user1.save()
                user2 = User(username='batman', email='batman@dc.com')
                user2.save()
                user3 = User(username='ironman', email='ironman@marvel.com')
                user3.save()
                user4 = User(username='spiderman', email='spiderman@marvel.com')
                user4.save()

                self.stdout.write('Creating teams...')
                team_dc = Team(name='Team DC')
                team_dc.save()
                team_marvel = Team(name='Team Marvel')
                team_marvel.save()
                team_dc.members.add(user1, user2)
                team_marvel.members.add(user3, user4)

                self.stdout.write('Creating workouts...')
                workout1 = Workout(name='Morning Cardio', description='A quick morning cardio routine.')
                workout1.save()
                workout2 = Workout(name='Strength Training', description='Full body strength workout.')
                workout2.save()
                workout1.suggested_for.add(user1, user3)
                workout2.suggested_for.add(user2, user4)

                self.stdout.write('Creating activities...')
                Activity.objects.create(
                    user=user1,
                    activity_type='Flying',
                    duration=60,
                    calories_burned=500,
                    date=timezone.now().date()
                )
                Activity.objects.create(
                    user=user2,
                    activity_type='Martial Arts',
                    duration=45,
                    calories_burned=400,
                    date=timezone.now().date()
                )
                Activity.objects.create(
                    user=user3,
                    activity_type='Engineering',
                    duration=90,
                    calories_burned=350,
                    date=timezone.now().date()
                )
                Activity.objects.create(
                    user=user4,
                    activity_type='Web Swinging',
                    duration=30,
                    calories_burned=250,
                    date=timezone.now().date()
                )

                self.stdout.write('Creating leaderboard...')
                Leaderboard.objects.create(user=user1, total_points=150, rank=1)
                Leaderboard.objects.create(user=user2, total_points=120, rank=2)
                Leaderboard.objects.create(user=user3, total_points=110, rank=3)
                Leaderboard.objects.create(user=user4, total_points=100, rank=4)

                self.stdout.write(self.style.SUCCESS('Database populated with superhero sample data.'))
        except IntegrityError as e:
            self.stderr.write(self.style.ERROR(f'Integrity error: {e}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))