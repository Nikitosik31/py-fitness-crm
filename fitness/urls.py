from django.urls import path

from .views import (
    index,
    TrainersListView,
    TrainersDetailView,
    TrainersCreateView,
    TrainersUpdateView,
    TrainersDeleteView,
    ClientListView,
    ClientDetailView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    ExerciseListView,
    ExerciseDetailView,
    ExerciseCreateView,
    ExerciseUpdateView,
    ExerciseDeleteView,
    WorkoutSessionListView,
    WorkoutSessionDetailView,
    WorkoutSessionCreateView,
    WorkoutSessionUpdateView,
    WorkoutSessionDeleteView,
    WorkoutProgramListView,
    WorkoutProgramDetailView,
    WorkoutProgramCreateView,
    WorkoutProgramUpdateView,
    WorkoutProgramDeleteView, RegisterView,
)

app_name = "fitness"
urlpatterns = [
    path("", index, name="index"),
    path("trainers/", TrainersListView.as_view(), name="trainers-list"),
    path(
        "trainers/<int:pk>/",
        TrainersDetailView.as_view(),
        name="trainers-detail",
    ),
    path(
        "trainers/create/",
        TrainersCreateView.as_view(),
        name="trainers-create",
    ),
    path(
        "trainers/<int:pk>/update-experience-years/",
        TrainersUpdateView.as_view(),
        name="trainers-update",
    ),
    path(
        "trainers/<int:pk>/delete-trainer/",
        TrainersDeleteView.as_view(),
        name="trainers-delete",
    ),
    path("clients/", ClientListView.as_view(), name="clients-list"),
    path(
        "clients/<int:pk>/", ClientDetailView.as_view(), name="clients-detail"
    ),
    path("clients/create/", ClientCreateView.as_view(), name="clients-create"),
    path(
        "clients/<int:pk>/update/",
        ClientUpdateView.as_view(),
        name="clients-update",
    ),
    path(
        "clients/<int:pk>/delete-client/",
        ClientDeleteView.as_view(),
        name="clients-delete",
    ),
    path("exercise/", ExerciseListView.as_view(), name="exercise-list"),
    path(
        "exercise/<int:pk>/",
        ExerciseDetailView.as_view(),
        name="exercise-detail",
    ),
    path(
        "exercise/create/",
        ExerciseCreateView.as_view(),
        name="exercise-create",
    ),
    path(
        "exercise/<int:pk>/update/",
        ExerciseUpdateView.as_view(),
        name="exercise-update",
    ),
    path(
        "exercise/<int:pk>/delete-exercise/",
        ExerciseDeleteView.as_view(),
        name="exercise-delete",
    ),
    path(
        "session/",
        WorkoutSessionListView.as_view(),
        name="workout-session-list",
    ),
    path(
        "session/<int:pk>/",
        WorkoutSessionDetailView.as_view(),
        name="workout-session-detail",
    ),
    path(
        "session/create/",
        WorkoutSessionCreateView.as_view(),
        name="workout-session-create",
    ),
    path(
        "session/<int:pk>/update/",
        WorkoutSessionUpdateView.as_view(),
        name="workout-session-update",
    ),
    path(
        "session/<int:pk>/delete-session/",
        WorkoutSessionDeleteView.as_view(),
        name="workout-session-delete",
    ),
    path(
        "program/",
        WorkoutProgramListView.as_view(),
        name="workout-program-list",
    ),
    path(
        "program/<int:pk>/",
        WorkoutProgramDetailView.as_view(),
        name="workout-program-detail",
    ),
    path(
        "program/create/",
        WorkoutProgramCreateView.as_view(),
        name="workout-program-create",
    ),
    path(
        "program/<int:pk>/update/",
        WorkoutProgramUpdateView.as_view(),
        name="workout-program-update",
    ),
    path(
        "program/<int:pk>/delete-program/",
        WorkoutProgramDeleteView.as_view(),
        name="workout-program-delete",
    ),
    path("register/", RegisterView.as_view(), name="register"),

]
