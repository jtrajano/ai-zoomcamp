from django.test import TestCase, Client
from django.urls import reverse
from .models import Task


class TaskViewTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.task1 = Task.objects.create(title="Test Task 1", description="Desc 1")
		self.task2 = Task.objects.create(title="Test Task 2", description="Desc 2", completed=True)

	def test_task_list_display(self):
		response = self.client.get(reverse('todo:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Test Task 1")
		self.assertContains(response, "Test Task 2")

	def test_create_task(self):
		response = self.client.post(
			reverse('todo:add'),
			{
				'title': 'New Task',
				'description': 'New Desc',
			},
			follow=True,
		)
		self.assertEqual(response.status_code, 200)
		t = Task.objects.filter(title='New Task').first()
		self.assertIsNotNone(t)
		# target_date removed; ensure task created
		self.assertEqual(t.description, 'New Desc')

	def test_toggle_complete(self):
		url = reverse('todo:toggle', args=[self.task1.pk])
		response = self.client.get(url, follow=True)
		self.assertEqual(response.status_code, 200)
		self.task1.refresh_from_db()
		self.assertTrue(self.task1.completed)

	def test_delete_task(self):
		url = reverse('todo:delete', args=[self.task2.pk])
		response = self.client.get(url, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertFalse(Task.objects.filter(pk=self.task2.pk).exists())

	def test_empty_title_not_created(self):
		response = self.client.post(
			reverse('todo:add'),
			{
				'title': '',
				'description': 'Should not be created',
			},
			follow=True,
		)
		self.assertEqual(response.status_code, 200)
		self.assertFalse(Task.objects.filter(description='Should not be created').exists())

	def test_edit_task(self):
		url = reverse('todo:edit', args=[self.task1.pk])
		response = self.client.post(
			url,
			{
				'title': 'Updated Title',
				'description': 'Updated Desc',
			},
			follow=True,
		)
		self.assertEqual(response.status_code, 200)
		self.task1.refresh_from_db()
		self.assertEqual(self.task1.title, 'Updated Title')
		self.assertEqual(self.task1.description, 'Updated Desc')
		# target_date removed; ensure description updated
		self.assertEqual(self.task1.description, 'Updated Desc')
