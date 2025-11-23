from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Task


def index(request):
	"""List tasks only."""
	tasks = Task.objects.all()
	return render(request, 'todo/index.html', {'tasks': tasks})


def toggle_complete(request, pk):
	"""Toggle the completed state of a task and redirect back to the list."""
	task = get_object_or_404(Task, pk=pk)
	task.completed = not task.completed
	task.save()
	return redirect('todo:index')


def delete_task(request, pk):
	"""Delete a task and redirect back to the list."""
	task = get_object_or_404(Task, pk=pk)
	task.delete()
	return redirect('todo:index')


def add_task(request):
	"""Show add form (GET) and create a new task (POST)."""
	if request.method == 'POST':
		title = request.POST.get('title', '').strip()
		description = request.POST.get('description', '').strip()
		if title:
			Task.objects.create(title=title, description=description)
			return redirect('todo:index')
		# If no title, re-render form (could add error handling)
	return render(request, 'todo/add.html')


def edit_task(request, pk):
	"""Show edit form (GET) and update task (POST)."""
	task = get_object_or_404(Task, pk=pk)
	if request.method == 'POST':
		title = request.POST.get('title', '').strip()
		description = request.POST.get('description', '').strip()
		if title:
			task.title = title
			task.description = description
			task.save()
			return redirect('todo:index')
		# If title empty, re-render form
	return render(request, 'todo/edit.html', {'task': task})
