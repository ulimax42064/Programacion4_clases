from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import Project, ProjectMembership, Task
from .repositories import TaskRepository


class TaskService:
    @staticmethod
    def mark_completed(task: Task) -> Task:
        if not task.due_date:
            raise ValidationError(
                "No se puede marcar una tarea como completada sin fecha límite registrada."
            )
        task.status = "completada"
        task.save(update_fields=["status"])
        return task

    @staticmethod
    def tasks_overdue(queryset=None):
        if queryset is None:
            queryset = TaskRepository.get_queryset()
        today = timezone.now().date()
        return queryset.filter(due_date__lt=today).exclude(status="completada")


class MembershipService:
    """Clase 7: única fuente de verdad para preguntas de membresía."""

    @staticmethod
    def is_member(user, project) -> bool:
        return ProjectMembership.objects.filter(project=project, user=user).exists()

    @staticmethod
    def is_admin(user, project) -> bool:
        return ProjectMembership.objects.filter(
            project=project, user=user, role="admin"
        ).exists()

    @staticmethod
    def projects_for(user):
        return (
            Project.objects.filter(memberships__user=user)
            .distinct()
            .order_by("id")
        )
