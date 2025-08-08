from django.urls import path
from . import views

urlpatterns = [
    path("", views.navegacion, name="navegacion"),
    path("index", views.index, name="frontend_index"),
    path("create", views.create, name="frontend_create"),
    path("show/<str:pk>", views.show, name="frontend_show"),
    path("edit/<str:pk>", views.edit, name="frontend_edit"),
    path("delete/<str:pk>", views.destroy, name="frontend_delete"),
    path("<str:pk>/createTask", views.createTask, name="frontend_createTask"),
    path("<str:pk>/showTask", views.showTask, name="frontend_showTask"),
    path("<str:pk>/editTask/<str:id>", views.editTask, name="frontend_editTask"),
    path("<str:pk>/deleteTask/<str:id>", views.destroyTask, name="frontend_deleteTask"),
    path(
        "<str:pk>/updateStatus/<str:id>",
        views.updateTaskStatus,
        name="frontend_updateStatus",
    ),
]
