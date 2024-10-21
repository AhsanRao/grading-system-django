from django.db import models
import enum
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError

# User = get_user_model()


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        FACULTY = "FACULTY", "Faculty"
        COORDINATOR = "COORDINATOR", "Coordinator"

    role = models.CharField(max_length=12, choices=Role.choices, default=Role.STUDENT)

    # role = models.CharField(max_length=10, choices=Role.choices, null=False)
    about = models.TextField(blank=True, null=True)

    @property
    def is_coordinator(self):
        return (
            self.groups.filter(name="Coordinator").exists()
            or self.role == User.Role.COORDINATOR
        )

    @property
    def is_faculty(self):
        return (
            self.groups.filter(name="Faculty").exists()
            or self.role == User.Role.FACULTY
        )

    @property
    def is_student(self):
        return (
            self.groups.filter(name="Student").exists()
            or self.role == User.Role.STUDENT
        )

    @property
    def is_supervisor(self):
        """Check if the user has any supervisor assignments."""
        return self.assigned_projects.filter(role="SUPERVISOR").exists()

    @property
    def is_examiner(self):
        """Check if the user has any examiner assignments."""
        return self.assigned_projects.filter(role="EXAMINER").exists()

    def is_supervisor_for_group(self, group_id):
        """Check if the user is a supervisor for a specific group."""
        return self.assigned_projects.filter(
            project_group_id=group_id, role="SUPERVISOR"
        ).exists()

    def is_examiner_for_group(self, group_id):
        """Check if the user is an examiner for a specific group."""
        return self.assigned_projects.filter(
            project_group_id=group_id, role="EXAMINER"
        ).exists()

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )


class StudentManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.STUDENT)


class Student(User):
    base_role = User.Role.STUDENT
    objects = StudentManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Welcome Student!"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)


class CoordinatorManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.COORDINATOR)


class Coordinator(User):
    base_role = User.Role.COORDINATOR
    objects = CoordinatorManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Welcome Coordinator!"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)


class FacultyManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.FACULTY)


class Faculty(User):
    base_role = User.Role.FACULTY
    objects = FacultyManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Welcome Faculty!"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)


def get_default_coordinator():
    return User.objects.get_or_create(username="default_coordiantor")[0].id


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    coordinator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="coordinated_projects",
        default=get_default_coordinator,  # Set a default coordinator function
    )

    def __str__(self):
        return self.name


class ProjectGroup(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="project_groups"
    )
    students = models.ManyToManyField(
        User,
        related_name="group_projects",
        limit_choices_to={"role": User.Role.STUDENT},
    )

    def __str__(self):
        return (
            f"{self.name} - {self.project.name}" if self.project_id else "Project Group"
        )

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the instance first, so it gets an ID

        if self.students.count() > 5:
            raise ValidationError("A project group cannot have more than 5 students.")

        # Check for student uniqueness across project groups
        if self.project_id:
            existing_student_ids = (
                ProjectGroup.objects.filter(project_id=self.project_id)
                .exclude(pk=self.pk)
                .values_list("students__id", flat=True)
            )
            new_student_ids = self.students.values_list("id", flat=True)
            duplicate_students = set(existing_student_ids) & set(new_student_ids)
            print(duplicate_students)
            # if duplicate_students:
            #     raise ValidationError("A student cannot be in more than one group in the same project.")


class FacultyAssignment(models.Model):
    project_group = models.ForeignKey(
        ProjectGroup, on_delete=models.CASCADE, related_name="assignments"
    )
    faculty = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assigned_projects"
    )
    role = models.CharField(
        max_length=10, choices=[("SUPERVISOR", "Supervisor"), ("EXAMINER", "Examiner")]
    )

    class Meta:
        unique_together = ("project_group", "faculty", "role")

    def __str__(self):
        return f"{self.faculty.get_username()} - {self.role} for {self.project_group.project.name} group"


class Grading(models.Model):
    project_group = models.ForeignKey(
        ProjectGroup, on_delete=models.CASCADE, related_name="gradings"
    )
    faculty = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gradings")
    grade_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def clean(self):
        total_grade = Grading.objects.filter(
            project_group=self.project_group
        ).aggregate(total=models.Sum("grade_percentage"))
        if total_grade["total"] and total_grade["total"] != 100:
            raise ValidationError(
                "Total grading percentage must equal 100% for the project group."
            )

    def __str__(self):
        return f"{self.grade_percentage}% by {self.faculty.get_full_name()} for {self.project_group}"


# Logbook assessment
class Logbook(models.Model):
    project_group = models.ForeignKey(
        ProjectGroup, on_delete=models.CASCADE, related_name="logbooks"
    )


class LogbookEntry(models.Model):
    logbook = models.ForeignKey(
        Logbook, on_delete=models.CASCADE, related_name="entries"
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="logbook_entries"
    )
    planning_score = models.DecimalField(max_digits=5, decimal_places=0)
    execution_score = models.DecimalField(max_digits=5, decimal_places=0)
    functionality_score = models.DecimalField(max_digits=5, decimal_places=0)

    class Meta:
        unique_together = ["logbook", "student"]


# Interview assessment
class Interview(models.Model):
    project_group = models.ForeignKey(
        ProjectGroup, on_delete=models.CASCADE, related_name="interviews"
    )


class InterviewEntry(models.Model):
    interview = models.ForeignKey(
        Interview, on_delete=models.CASCADE, related_name="entries"
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="interview_entries"
    )
    score = models.DecimalField(max_digits=5, decimal_places=0)

    class Meta:
        unique_together = ["interview", "student"]


# Proposal assessment
class Proposal(models.Model):
    project_group = models.ForeignKey(
        ProjectGroup, on_delete=models.CASCADE, related_name="proposals"
    )
    planning_score = models.DecimalField(max_digits=5, decimal_places=0)
    execution_score = models.DecimalField(max_digits=5, decimal_places=0)
    formatting_score = models.DecimalField(max_digits=5, decimal_places=0)
    presentation_score = models.DecimalField(max_digits=5, decimal_places=0)


class ProgressReport(models.Model):
    project_group = models.ForeignKey(
        ProjectGroup, on_delete=models.CASCADE, related_name="progress_reports"
    )
    formatting_score = models.DecimalField(max_digits=5, decimal_places=0)
    design_process_score = models.DecimalField(max_digits=5, decimal_places=0)


class MidProjectReport(models.Model):
    project_group = models.ForeignKey(
        ProjectGroup, on_delete=models.CASCADE, related_name="mid_project_reports"
    )
    formatting_score = models.DecimalField(max_digits=5, decimal_places=0)
    content_score = models.DecimalField(max_digits=5, decimal_places=0)
    design_selection_score = models.DecimalField(max_digits=5, decimal_places=0)
    conclusions_score = models.DecimalField(max_digits=5, decimal_places=0)


class MidProjectPresentation(models.Model):
    project_group = models.ForeignKey(
        ProjectGroup, on_delete=models.CASCADE, related_name="mid_project_presentations"
    )
    format_score = models.DecimalField(max_digits=5, decimal_places=0)
    technical_content_score = models.DecimalField(max_digits=5, decimal_places=0)
    qa_score = models.DecimalField(max_digits=5, decimal_places=0)
    comment = models.TextField(blank=True, null=True)


class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField()


# Examinar Models
class ExaminerMidProjectPresentation(models.Model):
    examiner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="examiner_presentations"
    )
    project_group = models.ForeignKey(
        "ProjectGroup",
        on_delete=models.CASCADE,
        related_name="examiner_mid_project_presentations",
    )
    format_score = models.DecimalField(
        max_digits=4,
        decimal_places=0,
        help_text="Max 20 - Formatting and clarity of presentation slides, completion of presentation on time.",
    )
    technical_content_score = models.DecimalField(
        max_digits=4,
        decimal_places=0,
        help_text="Max 40 - Covering all significant design steps, decisions, analysis and results.",
    )
    report_score = models.DecimalField(
        max_digits=4,
        decimal_places=0,
        help_text="Max 20 - Report formatting, report contents and conclusions.",
    )
    comment = models.TextField(blank=True, null=True)  # comment field

    def total_score(self):
        return self.format_score + self.technical_content_score + self.report_score


class ExaminerMidProjectPresentationQA(models.Model):
    presentation = models.ForeignKey(
        ExaminerMidProjectPresentation,
        on_delete=models.CASCADE,
        related_name="qa_scores",
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="examiner_presentation_qas"
    )
    qa_score = models.DecimalField(
        max_digits=4,
        decimal_places=0,
        help_text="Max 20 - Showing adequate knowledge and understanding of the subject and providing satisfying answers to questions.",
    )

    class Meta:
        unique_together = ("presentation", "student")

    def __str__(self):
        return f"{self.student} - QA Score: {self.qa_score}"
