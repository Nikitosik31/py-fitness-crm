from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from fitness.models import (
    Client,
    WorkoutProgram,
    Exercise,
    WorkoutSession,
    WorkoutType,
)


class ModelTest(TestCase):
    def setUp(self) -> None:
        self.trainer = get_user_model().objects.create_user(
            username="nik",
            password="test123",
            first_name="test_first",
            last_name="test_last",
        )

        self.test_client = Client.objects.create(
            first_name="test_first",
            last_name="test_last",
            age=22,
            weight=80,
            goal="test_goal",
        )

        self.exercise = Exercise.objects.create(
            name="test_exercise",
            muscle_group="test_muscle_group",
            description="test_exercise",
        )

        self.test_workout_program = WorkoutProgram.objects.create(
            name="test_workout_program",
            description="test_workout_program",
            workout_type=WorkoutType.objects.create(
                name="test_workout_type",
            ),
        )

    def test_trainer(self):

        self.assertEqual(
            str(self.trainer),
            f"{self.trainer.username} ({self.trainer.first_name} {self.trainer.last_name})",
        )

    def test_client(self):
        self.test_client.trainers.add(self.trainer)
        self.assertEqual(
            str(self.test_client),
            f"{self.test_client.first_name} {self.test_client.last_name}",
        )

    def test_workout_program(self):
        self.test_workout_program.exercises.add(self.exercise)
        self.assertEqual(
            str(self.test_workout_program), f"{self.test_workout_program.name}"
        )

    def test_workout_session(self):
        test_workout_session = WorkoutSession.objects.create(
            workout_program=self.test_workout_program,
            date=date.today(),
            duration_minutes=10,
            trainer=self.trainer,
            is_completed=False,
            max_participants=10,
        )
        test_workout_session.clients.add(self.test_client)
        self.assertEqual(
            str(test_workout_session),
            f"{test_workout_session.workout_program.name} - {test_workout_session.date}",
        )

    def test_exercise(self):
        self.assertEqual(str(self.exercise), f"{self.exercise.name}")
