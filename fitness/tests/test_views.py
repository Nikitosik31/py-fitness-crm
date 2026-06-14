from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from fitness.models import Client, WorkoutProgram, WorkoutType, WorkoutSession

TRAINER_URL = reverse("fitness:trainers-list")
CLIENT_URL = reverse("fitness:clients-list")
INDEX_URL = reverse("fitness:index")
PROGRAM_URL = reverse("fitness:workout-program-list")
SESSION_URL = reverse("fitness:workout-session-list")

class PublicTrainerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(TRAINER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTrainerTest(TestCase):
    def setUp(self) -> None:
        self.trainer = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client.force_login(self.trainer)

    def test_retrieve_trainer(self):
        response = self.client.get(TRAINER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["trainer_list"]), list(get_user_model().objects.all()))
        self.assertTemplateUsed(response, "fitness/trainer_list.html")


class PublicClientTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CLIENT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateClientTest(TestCase):
    def setUp(self) -> None:
        self.trainer = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client.force_login(self.trainer)

    def test_retrieve_trainer(self):
        Client.objects.create(
            first_name="test_first",
            last_name="test_last",
            age=10,
            weight=10,
            goal="test_goal",
        )
        response = self.client.get(CLIENT_URL)
        self.assertEqual(response.status_code, 200)
        client = Client.objects.all()
        self.assertEqual(
            list(response.context["client_list"]), list(client))
        self.assertTemplateUsed(response, "fitness/client_list.html")


class PublicIndexTest(TestCase):
    def test_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateIndexTest(TestCase):
    def setUp(self) -> None:
        self.trainer = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client.force_login(self.trainer)

    def test_retrieve_index(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "fitness/index.html")



class PublicWorkoutProgramTest(TestCase):
    def test_login_required(self):
        res = self.client.get(PROGRAM_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateWorkoutProgramTest(TestCase):
    def setUp(self) -> None:
        self.trainer = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client.force_login(self.trainer)

    def test_retrieve_workout_program(self):
        WorkoutProgram.objects.create(
            name="test_workout_program",
            description="test_workout_program",
            workout_type=WorkoutType.objects.create(
                name="test_workout_program",
            ),

        )
        response = self.client.get(PROGRAM_URL)
        self.assertEqual(response.status_code, 200)
        program = WorkoutProgram.objects.all()
        self.assertEqual(list(response.context["workoutprogram_list"]), list(program))
        self.assertTemplateUsed(response, "fitness/workout_program_list.html")


class PublicWorkoutSessionTest(TestCase):
    def test_login_required(self):
        res = self.client.get(SESSION_URL)
        self.assertNotEqual(res.status_code, 200)



class PrivateWorkoutSessionTest(TestCase):
    def setUp(self) -> None:
        self.trainer = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
        )
        self.client.force_login(self.trainer)

    def test_retrieve_workout_session(self):
        WorkoutSession.objects.create(
            workout_program=WorkoutProgram.objects.create(
                name="test_workout_session",
                description="test_workout_session",
                workout_type=WorkoutType.objects.create(
                    name="test_workout_session",
                )
            ),
            date=date.today(),
            duration_minutes=10,
            trainer=self.trainer,
            is_completed=False,
            max_participants=5,
        )

        response = self.client.get(SESSION_URL)
        self.assertEqual(response.status_code, 200)
        program = WorkoutSession.objects.all()
        self.assertEqual(list(response.context["workoutsession_list"]), list(program))
        self.assertTemplateUsed(response, "fitness/workout_session_list.html")


