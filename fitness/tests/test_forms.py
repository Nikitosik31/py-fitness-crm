from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from fitness.forms import TrainerCreateForm, TrainerExperienceYearsForm
from fitness.models import Specialization


class FormsTests(TestCase):
    def test_trainer_creation_form_with_specialization_experience_first_last_name_is_valid(
        self,
    ):
        specialization = Specialization.objects.create(
            name="test specialization",
        )
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "new user",
            "last_name": "user",
            "specialization": [specialization.pk],
            "experience_years": 2,
        }
        form = TrainerCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "new_user")
        self.assertEqual(form.cleaned_data["experience_years"], 2)
        self.assertEqual(form.cleaned_data["first_name"], "new user")
        self.assertEqual(form.cleaned_data["last_name"], "user")


class PrivateTrainerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123",
        )
        self.client.force_login(self.user)

    def test_create_trainer(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "new user",
            "last_name": "user",
            "experience_years": 2,
        }
        self.client.post(reverse("fitness:trainers-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(
            new_user.experience_years, form_data["experience_years"]
        )

    def test_experience_years_form_invalid(self):
        form = TrainerExperienceYearsForm(data={"experience_years": 1})
        self.assertFalse(form.is_valid())

    def test_experience_years_form_valid(self):
        form = TrainerExperienceYearsForm(data={"experience_years": 5})
        self.assertTrue(form.is_valid())
