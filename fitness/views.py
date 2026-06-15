from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.shortcuts import render

from fitness.forms import TrainerCreateForm, TrainerExperienceYearsForm, ClientCreateForm, WorkoutProgramCreateForm, \
    ExerciseCreateForm, WorkoutSessionCreateForm, TrainerSearchForm, ClientSearchForm, ExerciseSearchForm, \
    WorkoutProgramSearchForm, WorkoutSessionSearchForm
from fitness.models import Trainer, Client, Exercise, WorkoutProgram, WorkoutSession, Specialization, WorkoutType


@login_required
def index(request):
    """View function for the home page of the site."""

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
        "num_visits": num_visits + 1
    }

    return render(request,"fitness/index.html", context=context)


class TrainersListView(LoginRequiredMixin, generic.ListView):
    model = Trainer
    paginate_by = 5
    queryset = Trainer.objects.prefetch_related("clients")


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TrainersListView, self).get_context_data(**kwargs)
        trainer = self.request.GET.get("trainer", "")
        context["search_form"] = TrainerSearchForm(initial={"trainer": trainer})
        return context

    def get_queryset(self):
        queryset = Trainer.objects.prefetch_related("clients")
        form = TrainerSearchForm(self.request.GET)
        if form.is_valid():
            trainer = form.cleaned_data["trainer"]
            return queryset.filter(
                Q(first_name__icontains=trainer) |
                Q(last_name__icontains=trainer)
            )
        return queryset

class TrainersCreateView(LoginRequiredMixin, generic.CreateView):
    model = Trainer
    form_class = TrainerCreateForm
    success_url = reverse_lazy("fitness:trainers-list")


class TrainersDetailView(LoginRequiredMixin, generic.DetailView):
    model = Trainer
    queryset = Trainer.objects.all().prefetch_related("clients")

class TrainersUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Trainer
    form_class = TrainerExperienceYearsForm

class TrainersDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Trainer
    success_url = reverse_lazy("fitness:trainers-list")

class ClientListView(LoginRequiredMixin, generic.ListView):
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
                Q(first_name__icontains=client) |
                Q(last_name__icontains=client)
            )
        return queryset
class ClientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Client
    form_class = ClientCreateForm
    success_url = reverse_lazy("fitness:clients-list")

class ClientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Client
    queryset = Client.objects.all().prefetch_related("trainers")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        clients = self.object
        context["completed_workouts"] = (
            clients.workout_sessions.filter(is_completed=True).count()
        )

        context["upcoming_workouts"] = (
            clients.workout_sessions.filter(is_completed=False).count()
        )

        return context

class ClientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Client
    form_class = ClientCreateForm
    success_url = reverse_lazy("fitness:clients-list")

class ClientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Client
    success_url = reverse_lazy("fitness:clients-list")

class ExerciseListView(LoginRequiredMixin, generic.ListView):
    model = Exercise
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ExerciseListView, self).get_context_data(**kwargs)
        exercise = self.request.GET.get("exercise", "")
        context["search_form"] = ExerciseSearchForm(initial={"exercise": exercise})
        return context

    def get_queryset(self):
        queryset = Exercise.objects.all()
        form = ExerciseSearchForm(self.request.GET)
        if form.is_valid():
            exercise = form.cleaned_data["exercise"]
            return queryset.filter(name__icontains=exercise)
        return queryset


class ExerciseCreateView(LoginRequiredMixin, generic.CreateView):
    model = Exercise
    form_class = ExerciseCreateForm
    success_url = reverse_lazy("fitness:exercise-list")

class ExerciseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Exercise
    queryset = Exercise.objects.all()

class ExerciseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Exercise
    form_class = ExerciseCreateForm
    success_url = reverse_lazy("fitness:exercise-list")

class ExerciseDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Exercise
    success_url = reverse_lazy("fitness:exercise-list")


class WorkoutProgramListView(LoginRequiredMixin, generic.ListView):
    model = WorkoutProgram
    paginate_by = 5
    queryset = WorkoutProgram.objects.all().prefetch_related("exercises", "workout_sessions").select_related("workout_type")
    template_name = "fitness/workout_program_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkoutProgramListView, self).get_context_data(**kwargs)
        program = self.request.GET.get("program", "")
        context["search_form"] = WorkoutProgramSearchForm(initial={"workout_program": program})
        return context

    def get_queryset(self):
        queryset = WorkoutProgram.objects.prefetch_related("exercises", "workout_sessions")
        form = WorkoutProgramSearchForm(self.request.GET)
        if form.is_valid():
            program = form.cleaned_data["workout_program"]
            return queryset.filter(name__icontains=program)
        return queryset


class WorkoutProgramCreateView(LoginRequiredMixin, generic.CreateView):
    model = WorkoutProgram
    form_class = WorkoutProgramCreateForm
    success_url = reverse_lazy("fitness:workout-program-list")
    template_name = "fitness/workout_program_form.html"
class WorkoutProgramDetailView(LoginRequiredMixin, generic.DetailView):
    model = WorkoutProgram
    queryset = WorkoutProgram.objects.all().select_related("workout_type").prefetch_related("exercises")
    template_name = "fitness/workout_program_detail.html"

class WorkoutProgramUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = WorkoutProgram
    form_class = WorkoutProgramCreateForm
    success_url = reverse_lazy("fitness:workout-program-list")
    template_name = "fitness/workout_program_form.html"

class WorkoutProgramDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = WorkoutProgram
    success_url = reverse_lazy("fitness:workout-program-list")
    template_name = "fitness/workout_program_confirm_delete.html"

class WorkoutSessionListView(LoginRequiredMixin, generic.ListView):
    model = WorkoutSession
    paginate_by = 5
    queryset = WorkoutSession.objects.all().select_related("trainer", "workout_program").prefetch_related("clients")
    template_name = "fitness/workout_session_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkoutSessionListView, self).get_context_data(**kwargs)
        session = self.request.GET.get("session", "")
        context["search_form"] = WorkoutSessionSearchForm(initial={"workout_session": session})
        return context

    def get_queryset(self):
        queryset = WorkoutSession.objects.select_related("trainer", "workout_program").prefetch_related("clients")
        form = WorkoutSessionSearchForm(self.request.GET)

        if form.is_valid():
            session = form.cleaned_data.get("workout_session")
            if session:
                return queryset.filter(date=session)
        return queryset
class WorkoutSessionCreateView(LoginRequiredMixin, generic.CreateView):
    model = WorkoutSession
    form_class = WorkoutSessionCreateForm
    success_url = reverse_lazy("fitness:workout-session-list")
    template_name = "fitness/workout_session_form.html"

class WorkoutSessionDetailView(LoginRequiredMixin, generic.DetailView):
    model = WorkoutSession
    queryset = WorkoutSession.objects.select_related(
        "trainer",
        "workout_program"
    ).prefetch_related("clients")
    template_name = "fitness/workout_session_detail.html"

class WorkoutSessionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = WorkoutSession
    form_class = WorkoutSessionCreateForm
    success_url = reverse_lazy("fitness:workout-session-list")
    template_name = "fitness/workout_session_form.html"


class WorkoutSessionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = WorkoutSession
    success_url = reverse_lazy("fitness:workout-session-list")
    template_name = "fitness/workout_session_confirm_delete.html"


class SpecializationListView(generic.ListView):
    model = Specialization


class SpecializationCreateView(generic.CreateView):
    model = Specialization
    fields = "__all__"
    success_url = reverse_lazy("fitness:specialization-list")

class SpecializationUpdateView(generic.UpdateView):
    model = Specialization
    fields = "__all__"
    success_url = reverse_lazy("fitness:specialization-list")

class SpecializationDeleteView(generic.DeleteView):
    model = Specialization
    success_url = reverse_lazy("fitness:specialization-list")


class WorkoutTypeListView(generic.ListView):
    model = WorkoutType

class WorkoutTypeCreateView(generic.CreateView):
    model = WorkoutType
    fields = "__all__"
    success_url = reverse_lazy("fitness:workout-type-list")

class WorkoutTypeUpdateView(generic.UpdateView):
    model = WorkoutType
    fields = "__all__"
    success_url = reverse_lazy("fitness:workout-type-list")

class WorkoutTypeDetailView(generic.DetailView):
    model = WorkoutType

class WorkoutTypeDeleteView(generic.DeleteView):
    model = WorkoutType
    success_url = reverse_lazy("fitness:workout-type-list")

