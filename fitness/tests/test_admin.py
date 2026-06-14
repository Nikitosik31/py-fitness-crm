from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from fitness.models import Specialization


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.trainer = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.trainer)
        self.trainer = get_user_model().objects.create_user(
            username="author",
            password="testtest",
            experience_years=2,
        )
        specialization = Specialization.objects.create(
            name="Specialization",
        )
        self.trainer.specialization.add(specialization)


    def test_specialization_and_experience_years_list(self):
        """
        Test that trainers specialization and experience_years is in list_display on trainer admin page
        :return:
        """
        url = reverse("admin:fitness_trainer_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.trainer.experience_years)
        self.assertContains(res, self.trainer.specialization.first().name)

    def test_specialization_and_experience_years_detail(self):
        """
        Test that author's pseudonym is in list_display on trainer detail admin page
        :return:
        """
        url = reverse("admin:fitness_trainer_change", args=[self.trainer.id])
        res = self.client.get(url)

        self.assertContains(res, self.trainer.experience_years)
        self.assertContains(res, self.trainer.specialization.first().name)

        