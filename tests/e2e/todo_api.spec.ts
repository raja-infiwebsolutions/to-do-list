import { test, expect } from '@playwright/test';

// Base URL for the API
const BASE_URL = 'http://localhost:8000/api/todos/';

// Test for API endpoints

test.describe('API: Todo List', () => {
  test('GET /todos/ should return all todos', async ({ request }) => {
    const response = await request.get(BASE_URL);
    expect(response.status()).toBe(200);
    const todos = await response.json();
    expect(Array.isArray(todos)).toBe(true);
    await page.screenshot({ path: 'screenshots/get-todos.png' });
  });

  test('POST /todos/ should create a new todo', async ({ request }) => {
    const response = await request.post(BASE_URL, {
      data: { title: 'Test Todo', description: 'Test Description', completed: false, priority: 'low' },
    });
    expect(response.status()).toBe(201);
    const todo = await response.json();
    expect(todo).toHaveProperty('id');
    await page.screenshot({ path: 'screenshots/post-todo.png' });
  });

  test('GET /todos/{id}/ should return a single todo', async ({ request }) => {
    const response = await request.get(BASE_URL + '1/');
    expect(response.status()).toBe(200);
    const todo = await response.json();
    expect(todo).toHaveProperty('title');
    await page.screenshot({ path: 'screenshots/get-todo.png' });
  });

  test('PUT /todos/{id}/ should update a todo', async ({ request }) => {
    const response = await request.put(BASE_URL + '1/', {
      data: { title: 'Updated Todo', completed: true },
    });
    expect(response.status()).toBe(200);
    const todo = await response.json();
    expect(todo.completed).toBe(true);
    await page.screenshot({ path: 'screenshots/put-todo.png' });
  });

  test('DELETE /todos/{id}/ should delete a todo', async ({ request }) => {
    const response = await request.delete(BASE_URL + '1/');
    expect(response.status()).toBe(204);
    await page.screenshot({ path: 'screenshots/delete-todo.png' });
  });

  test('PATCH /todos/{id}/complete/ should mark todo as completed', async ({ request }) => {
    const response = await request.patch(BASE_URL + '1/complete/');
    expect(response.status()).toBe(200);
    const todo = await response.json();
    expect(todo.completed).toBe(true);
    await page.screenshot({ path: 'screenshots/patch-todo-complete.png' });
  });
});
