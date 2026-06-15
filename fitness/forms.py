from django import forms

from fitness.models import (
    Trainer,
    Client,
    WorkoutProgram,
    Exercise,
    WorkoutSession,
)


def validate_experience_years(experience_years):
    if experience_years <= 1:
        raise forms.ValidationError(
            "The trainer must have more than 1 year of experience."
        )


class TrainerCreateForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        ) + ("experience_years",)

    def clean_experience_years(self):
        experience_years = self.cleaned_data["experience_years"]
        validate_experience_years(experience_years)
        return experience_years


class TrainerExperienceYearsForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ("experience_years",)

    def clean_experience_years(self):
        experience_years = self.cleaned_data["experience_years"]
        validate_experience_years(experience_years)
        return experience_years


class ClientCreateForm(forms.ModelForm):
    trainers = forms.ModelMultipleChoiceField(
        queryset=Trainer.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Client
        fields = "__all__"


class WorkoutProgramCreateForm(forms.ModelForm):
    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = WorkoutProgram
        fields = "__all__"


class ExerciseCreateForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = "__all__"


class WorkoutSessionCreateForm(forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = WorkoutSession
        fields = "__all__"


class TrainerSearchForm(forms.Form):
    trainer = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search trainer ",
            }
        ),
    )


class ClientSearchForm(forms.Form):
    client = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search client ",
            }
        ),
    )


class ExerciseSearchForm(forms.Form):
    exercise = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search exercise",
            }
        ),
    )


class WorkoutProgramSearchForm(forms.Form):
    workout_program = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search workout program",
            }
        ),
    )


class WorkoutSessionSearchForm(forms.Form):
    workout_session = forms.DateField(
        required=False,
        label="",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
