from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import ProjectSerializer, TaskSerializer
from .models import Project, Task

# PROYECTOS


# LISTA DE PROYECTOS API
@api_view(["GET"])
def index(request):
    projects = Project.objects.all().order_by("id")
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


# CREAR PROYECTO
@api_view(["POST"])
def store(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


# DETALLE DE UN PROYECTO
@api_view(["GET"])
def show(request, pk):
    try:
        project = Project.objects.get(id=pk)
    except Project.DoesNotExist:
        return Response({"error": "Proyecto no encontrado"}, status=404)

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)


# ACTUALIZAR UN PROYECTO
@api_view(["PUT"])
def update(request, pk):
    try:
        project = Project.objects.get(id=pk)
    except Project.DoesNotExist:
        return Response({"PROYECTO NO ENCONTRADO"})

    serializer = ProjectSerializer(instance=project, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status=204)

    return Response(serializer.errors, status=400)


# ELIMINAR DE UN PROYECTO
@api_view(["DELETE"])
def destroy(request, pk):
    try:
        project = Project.objects.get(id=pk)
    except Project.DoesNotExist:
        return Response({"PROYECTO NO ENCONTRADO"})

    if project.tasks.exists():
        return Response({"No se puede eliminar un proyecto con tareas asociadas."})

    project.delete()
    return Response(status=204)


# TASK


# LISTA DE TAREAS
@api_view(["GET"])
def indexTask(request, project_id):
    tasks = Task.objects.filter(project_id=project_id).order_by("id")
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


# CREAR TAREA
@api_view(["POST"])
def storeTask(request, project_id):
    data = request.data.copy()
    data["project"] = project_id

    serializer = TaskSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# DETALLE DE UNA TAREA
@api_view(["GET"])
def showTask(request, project_id, pk):
    task = Task.objects.get(id=pk, project_id=project_id)
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
def updateTask(request, project_id, pk):
    task = Task.objects.get(id=pk, project_id=project_id)
    serializer = TaskSerializer(instance=task, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(status=204)
    return Response(serializer.errors, status=400)


# ELIMINAR DE UNA TAREA
@api_view(["DELETE"])
def destroyTask(request, project_id, pk):
    task = Task.objects.get(id=pk, project_id=project_id)

    task.delete()
    return Response(status=204)


# CAMBIAR DE ESTADO DE UNA TAREA
@api_view(["PATCH"])
def updateStatus(request, project_id, pk):
    task = Task.objects.get(id=pk, project_id=project_id)
    serializer = TaskSerializer(instance=task, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)
