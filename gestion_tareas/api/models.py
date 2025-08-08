from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Project(models.Model):
    STATUS_CHOICES = [
        ("active", "Activo"),
        ("completed", "Completado"),
        ("on_hold", "En pausa"),
    ]

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError(
                    "La fecha de fin no puede ser anterior a la fecha de inicio."
                )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "projects"


class Task(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("in_progress", "En Progreso"),
        ("completed", "Completado"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Bajo"),
        ("medium", "Medio"),
        ("high", "Alto"),
    ]

    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="tasks"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="medium"
    )
    due_date = models.DateField(blank=True, null=True)
    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.due_date:
            if self.due_date < timezone.now().date():
                raise ValidationError("La fecha limite debe ser futura.")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "tasks"
