"""Comprehensive tests for Todo API with full coverage."""

import pytest
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import datetime, timedelta

from .models import Todo


@pytest.mark.django_db
class TodoAPITests(APITestCase):
    """Test suite for Todo API endpoints."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        super().setUpClass()

    def setUp(self):
        """Set up test client and user for each test."""
        self.client = APIClient()
        # Create a test user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        
        # Create test todos
        self.todo1 = Todo.objects.create(
            title='Test Todo 1',
            description='Description 1',
            priority='high',
            completed=False
        )
        self.todo2 = Todo.objects.create(
            title='Test Todo 2',
            description='Description 2',
            priority='low',
            completed=True
        )
        self.todo3 = Todo.objects.create(
            title='Important Task',
            description='This is important',
            priority='medium',
            completed=False
        )

    def tearDown(self):
        """Clean up after tests."""
        Todo.objects.all().delete()
        User.objects.all().delete()

    # ─────────────────────────────────────────────────────────
    # LIST ENDPOINT TESTS
    # ─────────────────────────────────────────────────────────

    def test_list_todos_requires_authentication(self):
        """Test that list endpoint requires authentication."""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/todos/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_todos_returns_all(self):
        """Test listing all todos."""
        response = self.client.get('/api/todos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    def test_list_todos_with_completed_filter_true(self):
        """Test filtering todos by completed=true."""
        response = self.client.get('/api/todos/?completed=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], self.todo2.id)

    def test_list_todos_with_completed_filter_false(self):
        """Test filtering todos by completed=false."""
        response = self.client.get('/api/todos/?completed=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_list_todos_with_priority_filter(self):
        """Test filtering todos by priority."""
        response = self.client.get('/api/todos/?priority=high')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['priority'], 'high')

    def test_list_todos_with_search(self):
        """Test searching todos by text."""
        response = self.client.get('/api/todos/?search=Important')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Important Task')

    def test_list_todos_pagination(self):
        """Test pagination of todos list."""
        response = self.client.get('/api/todos/?page=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('results', response.data)

    def test_list_todos_invalid_completed_filter(self):
        """Test invalid completed filter value."""
        response = self.client.get('/api/todos/?completed=invalid')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ─────────────────────────────────────────────────────────
    # CREATE ENDPOINT TESTS
    # ─────────────────────────────────────────────────────────

    def test_create_todo_requires_authentication(self):
        """Test that create requires authentication."""
        self.client.force_authenticate(user=None)
        response = self.client.post('/api/todos/', {
            'title': 'New Todo',
            'description': 'Test',
            'priority': 'medium'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_todo_success(self):
        """Test creating a new todo."""
        data = {
            'title': 'New Todo',
            'description': 'A new test todo',
            'priority': 'medium',
            'completed': False
        }
        response = self.client.post('/api/todos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Todo')
        self.assertEqual(response.data['priority'], 'medium')

    def test_create_todo_minimal(self):
        """Test creating todo with only required field."""
        data = {'title': 'Minimal Todo'}
        response = self.client.post('/api/todos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['priority'], 'low')  # Default priority
        self.assertEqual(response.data['completed'], False)  # Default value

    def test_create_todo_missing_title(self):
        """Test create fails without title."""
        data = {'description': 'No title'}
        response = self.client.post('/api/todos/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_create_todo_empty_title(self):
        """Test create fails with empty title."""
        data = {'title': '   ', 'description': 'Empty title'}
        response = self.client.post('/api/todos/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_todo_invalid_priority(self):
        """Test create fails with invalid priority."""
        data = {
            'title': 'Test',
            'priority': 'invalid_priority'
        }
        response = self.client.post('/api/todos/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_todo_title_max_length(self):
        """Test creating todo with maximum title length."""
        long_title = 'a' * 255
        data = {'title': long_title}
        response = self.client.post('/api/todos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_todo_title_exceeds_max(self):
        """Test create fails when title exceeds max length."""
        long_title = 'a' * 256
        data = {'title': long_title}
        response = self.client.post('/api/todos/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ─────────────────────────────────────────────────────────
    # RETRIEVE ENDPOINT TESTS
    # ─────────────────────────────────────────────────────────

    def test_retrieve_todo_success(self):
        """Test retrieving a specific todo."""
        response = self.client.get(f'/api/todos/{self.todo1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.todo1.id)
        self.assertEqual(response.data['title'], self.todo1.title)

    def test_retrieve_nonexistent_todo(self):
        """Test retrieving non-existent todo."""
        response = self.client.get('/api/todos/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ─────────────────────────────────────────────────────────
    # UPDATE ENDPOINT TESTS
    # ─────────────────────────────────────────────────────────

    def test_update_todo_full(self):
        """Test full update (PUT) of a todo."""
        data = {
            'title': 'Updated Todo',
            'description': 'Updated description',
            'priority': 'high',
            'completed': True
        }
        response = self.client.put(f'/api/todos/{self.todo1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Todo')
        self.assertEqual(response.data['priority'], 'high')

    def test_update_todo_partial(self):
        """Test partial update (PATCH) of a todo."""
        data = {'priority': 'high'}
        response = self.client.patch(f'/api/todos/{self.todo1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['priority'], 'high')
        # Other fields should remain unchanged
        self.assertEqual(response.data['title'], self.todo1.title)

    def test_update_todo_invalid_priority(self):
        """Test update with invalid priority."""
        data = {'priority': 'ultra_high'}
        response = self.client.patch(f'/api/todos/{self.todo1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_nonexistent_todo(self):
        """Test updating non-existent todo."""
        data = {'title': 'Updated'}
        response = self.client.patch('/api/todos/99999/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ─────────────────────────────────────────────────────────
    # DELETE ENDPOINT TESTS
    # ─────────────────────────────────────────────────────────

    def test_delete_todo_success(self):
        """Test deleting a todo."""
        response = self.client.delete(f'/api/todos/{self.todo1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Todo.objects.filter(id=self.todo1.id).exists())

    def test_delete_nonexistent_todo(self):
        """Test deleting non-existent todo."""
        response = self.client.delete('/api/todos/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ─────────────────────────────────────────────────────────
    # CUSTOM ACTION TESTS
    # ─────────────────────────────────────────────────────────

    def test_complete_todo_action(self):
        """Test marking todo as completed."""
        self.assertEqual(self.todo1.completed, False)
        response = self.client.patch(f'/api/todos/{self.todo1.id}/complete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo1.refresh_from_db()
        self.assertTrue(self.todo1.completed)

    def test_uncomplete_todo_action(self):
        """Test marking completed todo as incomplete."""
        self.assertEqual(self.todo2.completed, True)
        response = self.client.patch(f'/api/todos/{self.todo2.id}/uncomplete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo2.refresh_from_db()
        self.assertFalse(self.todo2.completed)

    def test_complete_nonexistent_todo(self):
        """Test completing non-existent todo."""
        response = self.client.patch('/api/todos/99999/complete/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TodoModelTests(TestCase):
    """Test suite for Todo model."""

    def test_todo_creation(self):
        """Test creating a todo instance."""
        todo = Todo.objects.create(
            title='Test Todo',
            description='Test Description',
            priority='high'
        )
        self.assertEqual(todo.title, 'Test Todo')
        self.assertEqual(todo.priority, 'high')
        self.assertEqual(todo.completed, False)

    def test_todo_str_method(self):
        """Test Todo string representation."""
        todo = Todo.objects.create(title='Test Todo')
        self.assertEqual(str(todo), 'Test Todo')

    def test_todo_default_priority(self):
        """Test todo default priority is 'low'."""
        todo = Todo.objects.create(title='Test')
        self.assertEqual(todo.priority, 'low')

    def test_todo_timestamps(self):
        """Test that timestamps are set correctly."""
        todo = Todo.objects.create(title='Test')
        self.assertIsNotNone(todo.created_at)
        self.assertIsNotNone(todo.updated_at)
        self.assertEqual(todo.created_at, todo.updated_at)

    def test_todo_update_updates_timestamp(self):
        """Test that updating todo updates the updated_at timestamp."""
        todo = Todo.objects.create(title='Test')
        original_updated = todo.updated_at
        
        # Update the todo
        todo.title = 'Updated'
        todo.save()
        
        # Timestamp should be updated
        todo.refresh_from_db()
        self.assertGreaterEqual(todo.updated_at, original_updated)
