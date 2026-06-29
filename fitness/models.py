from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Trainer(AbstractUser):
    specialization = models.ManyToManyField(
        "Specialization", related_name="trainers"
    )
    experience_years = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "trainer"
        verbose_name_plural = "trainers"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("fitness:trainers-detail", kwargs={"pk": self.pk})


class Client(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    goal = models.TextField()
    trainers = models.ManyToManyField(Trainer, related_name="clients")
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client_profile",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["first_name", "last_name"]

    def get_absolute_url(self):
        return reverse("fitness:clients-detail", kwargs={"pk": self.pk})


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    muscle_group = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("fitness:exercise-detail", kwargs={"pk": self.pk})


class WorkoutSession(models.Model):
    clients = models.ManyToManyField(Client, related_name="workout_sessions")
    workout_program = models.ForeignKey(
        "WorkoutProgram",
        on_delete=models.CASCADE,
        related_name="workout_sessions",
    )
    date = models.DateField()
    duration_minutes = models.PositiveIntegerField()
    trainer = models.ForeignKey(
        Trainer, on_delete=models.CASCADE, related_name="workout_sessions"
    )
    is_completed = models.BooleanField(default=False)
    max_participants = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.workout_program.name} - {self.date}"

    def get_absolute_url(self):
        return reverse(
            "fitness:workout-session-detail", kwargs={"pk": self.pk}
        )


class WorkoutProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    exercises = models.ManyToManyField(
        Exercise, related_name="workout_programs"
    )
    workout_type = models.ForeignKey(
        "WorkoutType",
        on_delete=models.CASCADE,
        related_name="workout_programs",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "fitness:workout-program-detail", kwargs={"pk": self.pk}
        )


class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class WorkoutType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ProgressReport(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="reports"
    )
    date = models.DateField(auto_now_add=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    chest = models.DecimalField(max_digits=5, decimal_places=2)
    waist = models.DecimalField(max_digits=5, decimal_places=2)
    hips = models.DecimalField(max_digits=5, decimal_places=2)
    arm = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.client} - {self.date}"
