from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Task


def index(request):
	"""List tasks and handle creation of new tasks via POST."""
	if request.method == 'POST':
		title = request.POST.get('title', '').strip()
		description = request.POST.get('description', '').strip()
		if title:
			Task.objects.create(title=title, description=description)
		return redirect('todo:index')

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
