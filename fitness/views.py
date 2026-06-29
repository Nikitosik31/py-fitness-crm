
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import login

from fitness.forms import (
    TrainerCreateForm,
    TrainerExperienceYearsForm,
    ClientCreateForm,
    WorkoutProgramCreateForm,
    ExerciseCreateForm,
    WorkoutSessionCreateForm,
    TrainerSearchForm,
    ClientSearchForm,
    ExerciseSearchForm,
    WorkoutProgramSearchForm,
    WorkoutSessionSearchForm,
    ProgressReportForm, ClientRegisterForm,
)
from fitness.models import (
    Trainer,
    Client,
    Exercise,
    WorkoutProgram,
    WorkoutSession,
    ProgressReport,
)


@login_required
def index(request):
    if hasattr(request.user, "client_profile"):
        return redirect("fitness:client-profile")

    num_trainer = Trainer.objects.count()
    num_exercise = Exercise.objects.count()
    num_program = WorkoutProgram.objects.count()
    num_sessions = WorkoutSession.objects.count()
    num_clients = Client.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_trainer": num_trainer,
        "num_exercise": num_exercise,
        "num_program": num_program,
        "num_sessions": num_sessions,
        "num_clients": num_clients,
        "num_visits": num_visits + 1,
    }

    return render(request, "fitness/index.html", context=context)


class TrainerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, "client_profile"):
            return redirect("fitness:client-profile")
        return super().dispatch(request, *args, **kwargs)


class TrainersListView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.ListView
):
    model = Trainer
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        trainer = self.request.GET.get("trainer", "")
        context["search_form"] = TrainerSearchForm(
            initial={"trainer": trainer}
        )
        return context

    def get_queryset(self):
        queryset = Trainer.objects.prefetch_related(
            "clients", "specialization"
        )
        form = TrainerSearchForm(self.request.GET)
        if form.is_valid():
            trainer = form.cleaned_data["trainer"]
            return queryset.filter(
                Q(first_name__icontains=trainer)
                | Q(last_name__icontains=trainer)
            )
        return queryset


class TrainersCreateView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.CreateView
):
    model = Trainer
    form_class = TrainerCreateForm


class TrainersDetailView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.DetailView
):
    model = Trainer
    queryset = Trainer.objects.all().prefetch_related("clients")


class TrainersUpdateView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.UpdateView
):
    model = Trainer
    form_class = TrainerExperienceYearsForm


class TrainersDeleteView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.DeleteView
):
    model = Trainer
    success_url = reverse_lazy("fitness:trainers-list")


class ClientListView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.ListView
):
    model = Client
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.request.GET.get("client", "")
        context["search_form"] = ClientSearchForm(initial={"client": client})
        return context

    def get_queryset(self):
        queryset = Client.objects.prefetch_related("trainers").annotate(
            completed_workouts=Count(
                "workout_sessions",
                filter=Q(workout_sessions__is_completed=True),
                distinct=True,
            ),
            upcoming_workouts=Count(
                "workout_sessions",
                filter=Q(workout_sessions__is_completed=False),
                distinct=True,
            ),
        )
        form = ClientSearchForm(self.request.GET)
        if form.is_valid():
            client = form.cleaned_data["client"]
            return queryset.filter(
                Q(first_name__icontains=client)
                | Q(last_name__icontains=client)
            )
        return queryset


class ClientCreateView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.CreateView
):
    model = Client
    form_class = ClientCreateForm


class ClientDetailView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.DetailView
):
    model = Client
    queryset = Client.objects.prefetch_related("trainers").annotate(
        completed_workouts=Count(
            "workout_sessions",
            filter=Q(workout_sessions__is_completed=True),
            distinct=True,
        ),
        upcoming_workouts=Count(
            "workout_sessions",
            filter=Q(workout_sessions__is_completed=False),
            distinct=True,
        ),
    )


class ClientUpdateView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.UpdateView
):
    model = Client
    form_class = ClientCreateForm


class ClientDeleteView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.DeleteView
):
    model = Client
    success_url = reverse_lazy("fitness:clients-list")


class ExerciseListView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.ListView
):
    model = Exercise
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        exercise = self.request.GET.get("exercise", "")
        context["search_form"] = ExerciseSearchForm(
            initial={"exercise": exercise}
        )
        return context

    def get_queryset(self):
        queryset = Exercise.objects.all()
        form = ExerciseSearchForm(self.request.GET)
        if form.is_valid():
            exercise = form.cleaned_data["exercise"]
            return queryset.filter(name__icontains=exercise)
        return queryset


class ExerciseCreateView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.CreateView
):
    model = Exercise
    form_class = ExerciseCreateForm


class ExerciseDetailView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.DetailView
):
    model = Exercise
    queryset = Exercise.objects.all()


class ExerciseUpdateView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.UpdateView
):
    model = Exercise
    form_class = ExerciseCreateForm


class ExerciseDeleteView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.DeleteView
):
    model = Exercise
    success_url = reverse_lazy("fitness:exercise-list")


class WorkoutProgramListView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.ListView
):
    model = WorkoutProgram
    paginate_by = 5
    template_name = "fitness/workout_program_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        program = self.request.GET.get("program", "")
        context["search_form"] = WorkoutProgramSearchForm(
            initial={"workout_program": program}
        )
        return context

    def get_queryset(self):
        queryset = WorkoutProgram.objects.select_related(
            "workout_type"
        ).prefetch_related("exercises", "workout_sessions")
        form = WorkoutProgramSearchForm(self.request.GET)
        if form.is_valid():
            program = form.cleaned_data["workout_program"]
            return queryset.filter(name__icontains=program)
        return queryset


class WorkoutProgramCreateView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.CreateView
):
    model = WorkoutProgram
    form_class = WorkoutProgramCreateForm
    template_name = "fitness/workout_program_form.html"


class WorkoutProgramDetailView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.DetailView
):
    model = WorkoutProgram
    queryset = (
        WorkoutProgram.objects.all()
        .select_related("workout_type")
        .prefetch_related("exercises")
    )
    template_name = "fitness/workout_program_detail.html"


class WorkoutProgramUpdateView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.UpdateView
):
    model = WorkoutProgram
    form_class = WorkoutProgramCreateForm
    template_name = "fitness/workout_program_form.html"


class WorkoutProgramDeleteView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.DeleteView
):
    model = WorkoutProgram
    success_url = reverse_lazy("fitness:workout-program-list")
    template_name = "fitness/workout_program_confirm_delete.html"


class WorkoutSessionListView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.ListView
):
    model = WorkoutSession
    paginate_by = 5
    template_name = "fitness/workout_session_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.request.GET.get("session", "")
        context["search_form"] = WorkoutSessionSearchForm(
            initial={"workout_session": session}
        )
        return context

    def get_queryset(self):
        queryset = WorkoutSession.objects.select_related(
            "trainer", "workout_program"
        ).prefetch_related("clients")
        form = WorkoutSessionSearchForm(self.request.GET)

        if form.is_valid():
            session = form.cleaned_data.get("workout_session")
            if session:
                return queryset.filter(date=session)
        return queryset


class WorkoutSessionCreateView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.CreateView
):
    model = WorkoutSession
    form_class = WorkoutSessionCreateForm
    template_name = "fitness/workout_session_form.html"


class WorkoutSessionDetailView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.DetailView
):
    model = WorkoutSession
    queryset = WorkoutSession.objects.select_related(
        "trainer", "workout_program"
    ).prefetch_related("clients")
    template_name = "fitness/workout_session_detail.html"


class WorkoutSessionUpdateView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.UpdateView
):
    model = WorkoutSession
    form_class = WorkoutSessionCreateForm
    template_name = "fitness/workout_session_form.html"


class WorkoutSessionDeleteView(
    LoginRequiredMixin, TrainerRequiredMixin, generic.DeleteView
):
    model = WorkoutSession
    success_url = reverse_lazy("fitness:workout-session-list")
    template_name = "fitness/workout_session_confirm_delete.html"


class RegisterView(generic.CreateView):
    model = Trainer
    form_class = TrainerCreateForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("fitness:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


def client_create_view(request):
    if request.method == "POST":
        form = ClientRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(
                user=user,
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                age=form.cleaned_data["age"],
                weight=form.cleaned_data["weight"],
                goal=form.cleaned_data["goal"],
            )
            login(request, user)
            return redirect("fitness:client-profile")
    else:
        form = ClientRegisterForm()
    return render(request, "registration/client_register.html", {"form": form})


def redirect_after_login(request):
    if hasattr(request.user, "client_profile"):
        return redirect("fitness:client-profile")
    return redirect("fitness:index")


class ClientProfileView(LoginRequiredMixin, generic.DetailView):
    model = Client
    template_name = "fitness/client_profile.html"

    def get_object(self):
        return self.request.user.client_profile


class ProgressReportCreateView(LoginRequiredMixin, generic.CreateView):
    model = ProgressReport
    form_class = ProgressReportForm
    template_name = "fitness/progress_report_form.html"

    def form_valid(self, form):
        report = form.save(commit=False)
        report.client = self.request.user.client_profile
        report.save()
        return redirect("fitness:client-profile")
