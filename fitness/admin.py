from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Trainer,
    Client,
    Exercise,
    WorkoutProgram,
    WorkoutSession,
    Specialization,
    WorkoutType,
)


@admin.register(Trainer)
class TrainerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("get_specialization", "experience_years", )
    filter_horizontal = ("specialization",)
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "specialization",
                    "experience_years",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "specialization",
                    "experience_years",
                )
            },
        ),
    )


    def get_specialization(self, obj):
        return ", ".join(
            specialization.name
            for specialization in obj.specialization.all()
        )
    get_specialization.short_description = "Specializations"


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "age",
        "weight",
        "get_trainers"
    )
    search_fields = ("first_name", "last_name",)
    list_filter = ("trainers",)
    filter_horizontal = ("trainers",)

    def get_trainers(self, obj):
        return ", ".join(
            trainer.username
            for trainer in obj.trainers.all()
        )
    get_trainers.short_description = "Trainers"

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "muscle_group",)
    search_fields = ("name",)
    list_filter = ("muscle_group",)

@admin.register(WorkoutProgram)
class WorkoutProgramAdmin(admin.ModelAdmin):
    list_display = ("name", "workout_type")
    search_fields = ("name",)
    list_filter = ("workout_type",)


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = (
        "get_clients",
        "trainer",
        "workout_program",
        "date",
        "duration_minutes",
        "is_completed",
    )
    list_filter = (
        "date",
        "trainer",
        "is_completed"
    )
    search_fields = (
        "clients__first_name",
        "clients__last_name",
    )

    filter_horizontal = ("clients",)

    def get_clients(self, obj):

        return ", ".join(
            f"{client.first_name} {client.last_name}"
            for client in obj.clients.all()
        )
    get_clients.short_description = "Clients"

@admin.register(WorkoutType)
class WorkoutTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

admin.site.register(Specialization)