import { test, expect } from '@playwright/test';

test.describe('Feature: To-Do List Application', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('should load the page within 2 seconds', async ({ page }) => {
    const start = Date.now();
    await page.reload();
    const end = Date.now();
    expect(end - start).toBeLessThan(2000);
    await page.screenshot({ path: 'screenshots/page-load-time.png' });
  });

  test('should display all todos', async ({ page }) => {
    await page.waitForSelector('[data-testid="todo-list"]');
    const todos = await page.locator('[data-testid="todo-item"]').count();
    expect(todos).toBeGreaterThan(0);
    await page.screenshot({ path: 'screenshots/todos-display.png' });
  });

  test('should add a new todo', async ({ page }) => {
    await page.fill('[data-testid="new-todo-title"]', 'New Todo');
    await page.fill('[data-testid="new-todo-description"]', 'Description for new todo');
    await page.selectOption('[data-testid="new-todo-priority"]', 'medium');
    await page.fill('[data-testid="new-todo-due-date"]', '2023-12-31');
    await page.click('[data-testid="add-todo-btn"]');
    await expect(page.locator('[data-testid="todo-item"]').last()).toHaveText('New Todo');
    await page.screenshot({ path: 'screenshots/todo-add-success.png' });
  });

  test('should edit an existing todo', async ({ page }) => {
    await page.click('[data-testid="edit-todo-btn"]');
    await page.fill('[data-testid="edit-todo-title"]', 'Updated Todo');
    await page.click('[data-testid="save-todo-btn"]');
    await expect(page.locator('[data-testid="todo-item"]').first()).toHaveText('Updated Todo');
    await page.screenshot({ path: 'screenshots/todo-edit-success.png' });
  });

  test('should delete a todo with confirmation', async ({ page }) => {
    await page.click('[data-testid="delete-todo-btn"]');
    await page.click('[data-testid="confirm-delete-btn"]');
    await expect(page.locator('[data-testid="todo-item"]').count()).toBeLessThan(1);
    await page.screenshot({ path: 'screenshots/todo-delete-success.png' });
  });

  test('should filter todos by status', async ({ page }) => {
    await page.selectOption('[data-testid="filter-status"]', 'completed');
    const visibleTodos = await page.locator('[data-testid="todo-item"]').count();
    expect(visibleTodos).toBeGreaterThan(0);
    await page.screenshot({ path: 'screenshots/todo-filter-status.png' });
  });

  test('should sort todos by due date', async ({ page }) => {
    await page.selectOption('[data-testid="sort-options"]', 'due-date');
    const firstTodoDueDate = await page.locator('[data-testid="todo-item"]').first().getAttribute('data-due-date');
    // Add logic to check if the sorting is correct
    await page.screenshot({ path: 'screenshots/todo-sort-due-date.png' });
  });

  test('should toggle dark/light mode', async ({ page }) => {
    await page.click('[data-testid="toggle-theme-btn"]');
    const bodyClass = await page.evaluate(() => document.body.className);
    expect(bodyClass).toContain('dark');
    await page.screenshot({ path: 'screenshots/todo-toggle-theme.png' });
  });

  test('should show success notification on action', async ({ page }) => {
    await page.click('[data-testid="add-todo-btn"]');
    await expect(page.locator('[role="alert"]').first()).toBeVisible();
    await page.screenshot({ path: 'screenshots/todo-success-notification.png' });
  });

  test('should be accessible with no console errors', async ({ page }) => {
    const consoleErrors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });
    await page.reload();
    expect(consoleErrors.length).toBe(0);
    await page.screenshot({ path: 'screenshots/todo-no-console-errors.png' });
  });
});