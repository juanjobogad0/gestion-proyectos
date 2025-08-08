from django.shortcuts import render, redirect
import requests
from datetime import datetime
from django.contrib import messages
from django.core.paginator import Paginator


# INICIO
def navegacion(request):
    return render(request, "frontend/navegacion.html")


# LISTA DE PROYECTOS
def index(request):

    # filtros

    response = requests.get("http://127.0.0.1:8000/api/projects/")
    proyectos = response.json()

    filtro = request.GET.get("buscar_name", "").lower()

    lista = []
    for p in proyectos:
        nombre = p["name"].lower()

        if filtro in nombre:
            lista.append(p)

    proyectos = lista

    for proyecto in proyectos:
        proyecto["name"] = proyecto["name"].capitalize()
        proyecto["status"] = proyecto["status"].capitalize()

        proyecto["created_at"] = datetime.fromisoformat(
            proyecto["created_at"]
        ).strftime("%d/%m/%Y %H:%M")
        proyecto["updated_at"] = datetime.fromisoformat(
            proyecto["updated_at"]
        ).strftime("%d/%m/%Y %H:%M")

        tareas = proyecto.get("tasks", [])

        pendientes = 0
        completadas = 0
        en_progreso = 0

        for tarea in tareas:
            estado = tarea.get("status", "")
            if estado == "pending":
                pendientes += 1
            elif estado == "completed":
                completadas += 1
            elif estado == "in_progress":
                en_progreso += 1

        # PAGINACION
        proyecto["t_pendientes"] = pendientes
        proyecto["t_completadas"] = completadas
        proyecto["t_en_progreso"] = en_progreso

    page_number = request.GET.get("page", 1)
    paginator = Paginator(proyectos, 10)
    page_obj = paginator.get_page(page_number)

    return render(request, "frontend/index.html", {"page_obj": page_obj})


# CREAR PROYECTO
def create(request):
    if request.method == "POST":
        data = {
            "name": request.POST["name"],
            "description": request.POST["description"] or None,
            "status": request.POST["status"],
            "start_date": request.POST["start_date"],
            "end_date": request.POST["end_date"],
        }

        response = requests.post("http://127.0.0.1:8000/api/projects/store", data=data)

        if response.status_code == 201:
            messages.success(request, "Proyecto CREADO con exito!")
            return redirect("frontend_index")
        else:
            messages.error(request, "ERROR al crear el proyecto.")
            return redirect("frontend_index")

    return render(request, "frontend/nuevo_proyecto.html")


def show(request, pk):

    response = requests.get(f"http://127.0.0.1:8000/api/projects/{pk}")
    proyecto = response.json()

    proyecto["name"] = proyecto["name"].capitalize()
    proyecto["status"] = proyecto["status"].capitalize()
    proyecto["created_at"] = datetime.fromisoformat(proyecto["created_at"]).strftime(
        "%d/%m/%Y %H:%M"
    )
    proyecto["updated_at"] = datetime.fromisoformat(proyecto["updated_at"]).strftime(
        "%d/%m/%Y %H:%M"
    )

    tareas = proyecto.get("tasks", [])
    for tarea in tareas:
        tarea["title"] = tarea["title"].capitalize()
        tarea["status"] = tarea["status"].capitalize()

    contexto = {"proyecto": proyecto, "tarea": tareas}

    return render(request, "frontend/show.html", contexto)


# EDITAR PROYECTO
def edit(request, pk):

    response = requests.get(f"http://127.0.0.1:8000/api/projects/{pk}")
    proyecto = response.json()

    if request.method == "POST":
        data = {
            "name": request.POST["name"],
            "description": request.POST["description"],
            "status": request.POST["status"],
            "start_date": request.POST["start_date"],
            "end_date": request.POST["end_date"],
        }

        response = requests.put(
            f"http://127.0.0.1:8000/api/projects/{pk}/update", data=data
        )
        if response.status_code == 204:
            messages.success(request, "Proyecto EDITADO con exito!")
            return redirect("frontend_index")

        else:
            messages.error(request, "No fue posible EDITAR")
            return redirect("frontend_index")

    return render(request, "frontend/edit.html", {"proyecto": proyecto})


# ELIMINAR PROYECTO
def destroy(request, pk):
    response = requests.delete(f"http://127.0.0.1:8000/api/projects/{pk}/delete")

    if response.status_code == 204:
        messages.success(request, "Proyecto eliminado con exito!")
        return redirect("frontend_index")

    else:
        messages.error(request, "NO se puede ELIMINAR un Proyecto con tareas")
    return redirect("frontend_index")


# CREAR TAREA
def createTask(request, pk):

    if request.method == "POST":
        data = {
            "project": request.POST["project"],
            "title": request.POST["title"],
            "description": request.POST["description"] or None,
            "status": request.POST["status"],
            "priority": request.POST["priority"],
            "due_date": request.POST["due_date"] or None,
            "assigned_to": request.POST["assigned_to"] or None,
        }

        response = requests.post(
            f"http://127.0.0.1:8000/api/projects/{pk}/tasks/create", data=data
        )

        if response.status_code == 201:
            messages.success(request, "Tarea CREADA!")
            return redirect("frontend_show", pk=pk)
        else:
            messages.error(request, "Error al crear la Tarea.")
            return redirect("frontend_show", pk=pk)

    return render(request, "frontend/createTask.html", {"pk": pk})


# LISTA DE TAREAS DE UN PROYECTO
def showTask(request, pk):
    response = requests.get(f"http://127.0.0.1:8000/api/projects/{pk}/tasks")
    tareas = response.json()

    for tarea in tareas:
        tarea["title"] = tarea["title"].capitalize()
        tarea["status"] = tarea["status"].capitalize()
        tarea["priority"] = tarea["priority"].capitalize()
        tarea["assigned_to"] = tarea["assigned_to"]

        tarea["created_at"] = datetime.fromisoformat(tarea["created_at"]).strftime(
            "%d/%m/%Y %H:%M"
        )
        tarea["updated_at"] = datetime.fromisoformat(tarea["updated_at"]).strftime(
            "%d/%m/%Y %H:%M"
        )

    return render(request, "frontend/showTask.html", {"tareas": tareas})


# EDITAR UNA TAREA
def editTask(request, pk, id):

    response = requests.get(f"http://127.0.0.1:8000/api/projects/{pk}/tasks/{id}")
    tarea = response.json()

    if request.method == "POST":
        data = {
            "title": request.POST["title"],
            "description": request.POST["description"],
            "status": request.POST["status"],
            "priority": request.POST["priority"],
            "due_date": request.POST["due_date"],
            "assigned_to": request.POST["assigned_to"],
        }

        response = requests.put(
            f"http://127.0.0.1:8000/api/projects/{pk}/tasks/{id}/updateTask", data=data
        )
        if response.status_code == 204:
            messages.success(request, "Tarea EDITADA con exito!")
            return redirect("frontend_showTask", pk=pk)
        else:
            messages.error(request, "No fue posible EDITAR")
            return redirect("frontend_showTask", pk=pk)

    return render(
        request, "frontend/editTask.html", {"pk": pk, "id": id, "tarea": tarea}
    )


# ELIMINAR UNA TAREA
def destroyTask(request, pk, id):
    response = requests.delete(
        f"http://127.0.0.1:8000/api/projects/{pk}/tasks/{id}/delete"
    )

    if response.status_code == 204:
        messages.success(request, "Tarea ELIMINADA")
        return redirect("frontend_showTask", pk=pk)

    messages.error(request, "No se pudo eliminar")
    return redirect("frontend_showTask", pk=pk)


# ACTUALIZAR ESTADO DE UNA TAREA
def updateTaskStatus(request, pk, id):
    if request.method == "POST":
        print("POST DATA:", request.POST)
        data = {
            "status": request.POST["status"],
        }

        response = requests.patch(
            f"http://127.0.0.1:8000/api/projects/{pk}/tasks/{id}/updateStatus",
            data=data,
        )

        if response.status_code == 200:
            messages.success(request, "¡Estado actualizado con éxito!")
        else:
            messages.error(request, "Ocurrió un error al actualizar el estado.")

    return redirect("frontend_show", pk=pk)
