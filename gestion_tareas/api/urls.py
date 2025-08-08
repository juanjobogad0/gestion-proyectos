from django.urls import path
from . import views

urlpatterns = [
    ## PROYECTOS ##
    path("projects/", views.index, name="api_index"),  # TODOS LOS PROYECTOS
    path("projects/store", views.store, name="api_store"),  # CREAR NUEVO PROYECTO
    path("projects/<str:pk>", views.show, name="api_show"),  # DETALLE DE UN PROYECTO
    path(
        "projects/<str:pk>/update", views.update, name="api_update"
    ),  # ACTUALIZAR UN PROYECTO
    path(
        "projects/<str:pk>/delete", views.destroy, name="api_delete"
    ),  # ELIMINAR UN PROYECTO
    ## TAREAS ##
    path(
        "projects/<str:project_id>/tasks", views.indexTask, name="api_indexTask"
    ),  # TODOS LAS TAREAS DE UN PROYECTO
    path(
        "projects/<str:project_id>/tasks/create", views.storeTask, name="api_storeTask"
    ),  # CREAR NUEVA TAREA
    path(
        "projects/<str:project_id>/tasks/<str:pk>", views.showTask, name="api_showTask"
    ),  # DETALLE DE UNA TAREA
    path(
        "projects/<str:project_id>/tasks/<str:pk>/updateTask",
        views.updateTask,
        name="api_updateTask",
    ),  # ACTUALIZAR UNA TAREA
    path(
        "projects/<str:project_id>/tasks/<str:pk>/delete",
        views.destroyTask,
        name="api_destroyTask",
    ),  # ELIMINAR UNA TAREA
    path(
        "projects/<str:project_id>/tasks/<str:pk>/updateStatus",
        views.updateStatus,
        name="api_updateStatus",
    ),  # ACTUALIZAR ESTADO DE UNA TAREA
]
