from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    PasswordChangeForm,
    UsernameField,
)
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class StudentRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        label=_("Password Confirmation"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Password Confirmation",
            }
        ),
    )

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Username"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.STUDENT
        if commit:
            user.save()
        return user


class CoordinatorRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        label=_("Password Confirmation"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Password Confirmation",
            }
        ),
    )

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Username"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.COORDINATOR
        if commit:
            user.save()
        return user


class FacultyRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        label=_("Password Confirmation"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Password Confirmation",
            }
        ),
    )

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Username"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.FACULTY
        if commit:
            user.save()
        return user


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        label=_("Password Confirmation"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Password Confirmation",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "Username",
                }
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control form-control-lg", "placeholder": "Email"}
            ),
        }


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "Username"}
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "Password"}
        ),
    )


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control form-control-lg", "placeholder": "Email"}
        )
    )


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "New Password",
            }
        ),
        label="New Password",
    )
    new_password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Confirm New Password",
            }
        ),
        label="Confirm New Password",
    )


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Old Password",
            }
        ),
        label="New Password",
    )
    new_password1 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "New Password",
            }
        ),
        label="New Password",
    )
    new_password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Confirm New Password",
            }
        ),
        label="Confirm New Password",
    )


from .models import Project
from .models import ProjectGroup, User

from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            if field_name == "description":
                field.widget = forms.Textarea(
                    attrs={"class": "form-control", "rows": 3}
                )


class ProjectGroupForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role=User.Role.STUDENT),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        required=False,
    )

    class Meta:
        model = ProjectGroup
        fields = ["name", "students"]

    def __init__(self, *args, **kwargs):
        super(ProjectGroupForm, self).__init__(*args, **kwargs)
        self.fields["name"].label = "Project Group"
        self.fields["students"].label = "Select Students"
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = (
                "form-check-input" if field_name == "students" else "form-control"
            )


from .models import LogbookEntry
from django.forms import modelformset_factory


class ReadOnlyMixin:
    def set_readonly(self):
        for field_name in self.fields:
            self.fields[field_name].disabled = True


class LogbookEntryForm(ReadOnlyMixin, forms.ModelForm):
    class Meta:
        model = LogbookEntry
        fields = ["student", "planning_score", "execution_score", "functionality_score"]
        widgets = {
            "planning_score": forms.NumberInput(attrs={"class": "form-control"}),
            "execution_score": forms.NumberInput(attrs={"class": "form-control"}),
            "functionality_score": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        readonly = kwargs.pop("readonly", False)
        project_group = kwargs.pop("project_group", None)
        super().__init__(*args, **kwargs)
        if project_group:
            self.fields["student"].queryset = project_group.students.all()
            self.fields["student"].widget.attrs.update({"class": "form-control"})
        if readonly:
            self.set_readonly()


# Generate a formset for logbook entries
LogbookEntryFormSet = forms.modelformset_factory(
    LogbookEntry, form=LogbookEntryForm, extra=0, can_delete=True
)

from .models import InterviewEntry


class InterviewEntryForm(ReadOnlyMixin, forms.ModelForm):
    class Meta:
        model = InterviewEntry
        fields = ["student", "score"]
        widgets = {
            "score": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        readonly = kwargs.pop("readonly", False)
        project_group = kwargs.pop("project_group", None)
        super().__init__(*args, **kwargs)
        if project_group:
            self.fields["student"].queryset = project_group.students.all()
            self.fields["student"].widget.attrs.update({"class": "form-control"})
        if readonly:
            self.set_readonly()


# Create the formset for InterviewEntry forms
InterviewEntryFormSet = modelformset_factory(
    InterviewEntry, form=InterviewEntryForm, extra=0, can_delete=True
)

from .models import Proposal


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = [
            "planning_score",
            "execution_score",
            "formatting_score",
            "presentation_score",
        ]
        labels = {
            "planning_score": "Project Planning (Max 15 points)",
            "execution_score": "Project Execution (Max 60 points)",
            "formatting_score": "Proposal Formatting (Max 15 points)",
            "presentation_score": "Presentation (Max 10 points)",
        }
        help_texts = {
            "planning_score": "Score for GANTT chart, PERT chart, and literature review.",
            "execution_score": "Score for system functionality, failure modes, and environmental issues.",
            "formatting_score": "Score for the correct numbering and labeling of tables and figures, and proper citation.",
            "presentation_score": "Score for covering all topics within allocated time and presenting material clearly.",
        }

    def clean_planning_score(self):
        planning_score = self.cleaned_data.get("planning_score")
        if planning_score < 0 or planning_score > 15:
            raise ValidationError("Project Planning score must be between 0 and 15.")
        return planning_score

    def clean_execution_score(self):
        execution_score = self.cleaned_data.get("execution_score")
        if execution_score < 0 or execution_score > 60:
            raise ValidationError("Project Execution score must be between 0 and 60.")
        return execution_score

    def clean_formatting_score(self):
        formatting_score = self.cleaned_data.get("formatting_score")
        if formatting_score < 0 or formatting_score > 15:
            raise ValidationError("Proposal Formatting score must be between 0 and 15.")
        return formatting_score

    def clean_presentation_score(self):
        presentation_score = self.cleaned_data.get("presentation_score")
        if presentation_score < 0 or presentation_score > 10:
            raise ValidationError("Presentation score must be between 0 and 10.")
        return presentation_score

    def clean(self):
        cleaned_data = super().clean()
        total_score = sum(
            cleaned_data.get(field, 0)
            for field in [
                "planning_score",
                "execution_score",
                "formatting_score",
                "presentation_score",
            ]
        )
        if total_score > 100:
            raise ValidationError("Total score for Proposal cannot exceed 100.")
        return cleaned_data


from .models import ProgressReport, MidProjectReport, MidProjectPresentation
from django.core.exceptions import ValidationError


class ProgressReportForm(forms.ModelForm):
    class Meta:
        model = ProgressReport
        fields = ["formatting_score", "design_process_score"]
        labels = {
            "formatting_score": "Report Formatting (Max 30 points)",
            "design_process_score": "Design Process (Max 70 points)",
        }
        help_texts = {
            "formatting_score": "Score for the formatting of tables, figures, and proper citation.",
            "design_process_score": "Score for objectives, decision matrix, and first cost estimate of the system.",
        }

    def clean_formatting_score(self):
        formatting_score = self.cleaned_data.get("formatting_score")
        if formatting_score is not None and (
            formatting_score < 0 or formatting_score > 30
        ):
            raise ValidationError("Formatting score must be between 0 and 30.")
        return formatting_score

    def clean_design_process_score(self):
        design_process_score = self.cleaned_data.get("design_process_score")
        if design_process_score is not None and (
            design_process_score < 0 or design_process_score > 70
        ):
            raise ValidationError("Design process score must be between 0 and 70.")
        return design_process_score

    def clean(self):
        cleaned_data = super().clean()
        total_score = sum(cleaned_data.get(field, 0) for field in self.fields)
        if total_score > 100:
            raise ValidationError("Total score for Progress Report cannot exceed 100.")
        return cleaned_data


class MidProjectReportForm(forms.ModelForm):
    class Meta:
        model = MidProjectReport
        fields = [
            "formatting_score",
            "content_score",
            "design_selection_score",
            "conclusions_score",
        ]
        labels = {
            "formatting_score": "Report Formatting (Max 15 points)",
            "content_score": "Report Content (Max 60 points)",
            "design_selection_score": "Design Selection Process (Max 15 points)",
            "conclusions_score": "Conclusions (Max 10 points)",
        }
        help_texts = {
            "formatting_score": "Score for correctly numbered and labeled tables and figures.",
            "content_score": "Score for literature review, modeling, analysis results, and discussion.",
            "design_selection_score": "Score for the correct design selection process reflecting the selection of a particular design.",
            "conclusions_score": "Score for the discussion and conclusions section of your report.",
        }

    def clean_formatting_score(self):
        formatting_score = self.cleaned_data.get("formatting_score")
        if formatting_score < 0 or formatting_score > 15:
            raise ValidationError("Formatting score must be between 0 and 15.")
        return formatting_score

    def clean_content_score(self):
        content_score = self.cleaned_data.get("content_score")
        if content_score < 0 or content_score > 60:
            raise ValidationError("Content score must be between 0 and 60.")
        return content_score

    def clean_design_selection_score(self):
        design_selection_score = self.cleaned_data.get("design_selection_score")
        if design_selection_score < 0 or design_selection_score > 15:
            raise ValidationError(
                "Design selection process score must be between 0 and 15."
            )
        return design_selection_score

    def clean_conclusions_score(self):
        conclusions_score = self.cleaned_data.get("conclusions_score")
        if conclusions_score < 0 or conclusions_score > 10:
            raise ValidationError("Conclusions score must be between 0 and 10.")
        return conclusions_score

    def clean(self):
        cleaned_data = super().clean()
        total_score = sum(cleaned_data.get(field, 0) for field in self.fields)
        if total_score > 100:
            raise ValidationError(
                "Total score for the Mid-Project Report cannot exceed 100."
            )
        return cleaned_data


class MidProjectPresentationForm(forms.ModelForm):
    class Meta:
        model = MidProjectPresentation
        fields = ["format_score", "technical_content_score", "qa_score", "comment"]
        labels = {
            "format_score": "Presentation Format (Max 40 points)",
            "technical_content_score": "Technical Content (Max 40 points)",
            "qa_score": "Q&A (Max 20 points)",
            "comment": "Additional Comments",
        }
        help_texts = {
            "format_score": "Score for the formatting and clarity of presentation slides, and completion of presentation in a timely manner.",
            "technical_content_score": "Score for covering all significant design steps, decisions, analysis and results.",
            "qa_score": "Score for showing adequate knowledge and understanding of the subject, and providing satisfying answers to questions.",
            "comment": "Enter any additional comments here.",
        }
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3})  # Ensure textarea for comment
        }

    def clean_format_score(self):
        format_score = self.cleaned_data.get("format_score")
        if format_score < 0 or format_score > 40:
            raise ValidationError("Format score must be between 0 and 40.")
        return format_score

    def clean_technical_content_score(self):
        technical_content_score = self.cleaned_data.get("technical_content_score")
        if technical_content_score < 0 or technical_content_score > 40:
            raise ValidationError("Technical content score must be between 0 and 40.")
        return technical_content_score

    def clean_qa_score(self):
        qa_score = self.cleaned_data.get("qa_score")
        if qa_score < 0 or qa_score > 20:
            raise ValidationError("Q&A score must be between 0 and 20.")
        return qa_score

    def clean(self):
        cleaned_data = super().clean()
        score_fields = ["format_score", "technical_content_score", "qa_score"]
        total_score = sum(
            cleaned_data.get(field, 0)
            for field in score_fields
            if field in cleaned_data
        )
        if total_score > 100:
            raise ValidationError(
                "Total score for the Mid-Project Presentation cannot exceed 100."
            )
        return cleaned_data


from .models import ExaminerMidProjectPresentation, ExaminerMidProjectPresentationQA


class ExaminerMidProjectPresentationForm(forms.ModelForm):
    class Meta:
        model = ExaminerMidProjectPresentation
        fields = ["format_score", "technical_content_score", "report_score", "comment"]
        labels = {
            "format_score": "Presentation Formatting (Max 20 points)",
            "technical_content_score": "Technical Content (Max 40 points)",
            "report_score": "Mid-Project Report (Max 20 points)",
            "comment": "Additional Comments",
        }
        help_texts = {
            "format_score": "Score for formatting and clarity of presentation slides, completion on time. Speaking in a clear, audible, and understandable voice.",
            "technical_content_score": "Score for covering all significant design steps, decisions, analysis and results.",
            "report_score": "Score for report formatting, contents, and conclusions.",
            "comment": "Enter any additional comments here.",
        }

        widgets = {
            "comment": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Enter any relevant comments here..."}
            )  # Textarea for comments
        }

    def clean_format_score(self):
        format_score = self.cleaned_data.get("format_score")
        if format_score < 0 or format_score > 20:
            raise ValidationError(
                "Presentation Formatting score must be between 0 and 20."
            )
        return format_score

    def clean_technical_content_score(self):
        technical_content_score = self.cleaned_data.get("technical_content_score")
        if technical_content_score < 0 or technical_content_score > 40:
            raise ValidationError("Technical Content score must be between 0 and 40.")
        return technical_content_score

    def clean_report_score(self):
        report_score = self.cleaned_data.get("report_score")
        if report_score < 0 or report_score > 20:
            raise ValidationError("Mid-Project Report score must be between 0 and 20.")
        return report_score

    def clean(self):
        cleaned_data = super().clean()
        total_score = sum(
            cleaned_data.get(field, 0)
            for field in ["format_score", "technical_content_score", "report_score"]
        )
        if total_score > 100:
            raise ValidationError(
                "Total score for Mid-Project Presentation cannot exceed 100."
            )
        return cleaned_data


class ExaminerMidProjectPresentationQAForm(forms.ModelForm):
    class Meta:
        model = ExaminerMidProjectPresentationQA
        fields = ["student", "qa_score"]
        widgets = {
            "qa_score": forms.NumberInput(
                attrs={
                    "type": "number",
                    "step": "1",
                    "min": "0",
                    "max": "20",
                    "class": "form-control",
                }
            ),
            "student": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        readonly = kwargs.pop("readonly", False)
        project_group = kwargs.pop("project_group", None)
        super(ExaminerMidProjectPresentationQAForm, self).__init__(*args, **kwargs)
        if project_group:
            # Ensuring that only students from the specific project group are selectable
            self.fields["student"].queryset = project_group.students.all()
            self.fields["student"].widget.attrs.update({"class": "form-control"})
        if readonly:
            self.set_readonly()

    def clean_qa_score(self):
        qa_score = self.cleaned_data.get("qa_score")
        if qa_score < 0 or qa_score > 20:
            raise ValidationError("QA score must be between 0 and 20.")
        return qa_score


# Create a formset for ExaminerMidProjectPresentationQA forms
ExaminerMidProjectPresentationQAFormSet = modelformset_factory(
    ExaminerMidProjectPresentationQA,
    form=ExaminerMidProjectPresentationQAForm,
    extra=0,
    can_delete=True,
)

for form in [
    ProposalForm,
    ProgressReportForm,
    MidProjectReportForm,
    MidProjectPresentationForm,
    ExaminerMidProjectPresentationForm,
]:
    setattr(
        form,
        "__init__",
        lambda self, *args, **kwargs: self._init_with_bootstrap_classes(
            *args, **kwargs
        ),
    )


def _init_with_bootstrap_classes(self, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)
    for field in self.fields.values():
        if isinstance(field.widget, forms.CheckboxSelectMultiple):
            css_class = "form-check-input"
        else:
            css_class = "form-control"
        field.widget.attrs.update({"class": css_class})


# Assign the shared init method to each form class
ProposalForm._init_with_bootstrap_classes = _init_with_bootstrap_classes
MidProjectReportForm._init_with_bootstrap_classes = _init_with_bootstrap_classes
MidProjectPresentationForm._init_with_bootstrap_classes = _init_with_bootstrap_classes
ProgressReportForm._init_with_bootstrap_classes = _init_with_bootstrap_classes
ExaminerMidProjectPresentationForm._init_with_bootstrap_classes = (
    _init_with_bootstrap_classes
)

from .models import FacultyAssignment


class FacultyAssignmentForm(forms.ModelForm):
    class Meta:
        model = FacultyAssignment
        fields = ["faculty", "role"]
        widgets = {
            "faculty": forms.Select(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(FacultyAssignmentForm, self).__init__(*args, **kwargs)
        self.fields["faculty"].queryset = User.objects.filter(role=User.Role.FACULTY)
