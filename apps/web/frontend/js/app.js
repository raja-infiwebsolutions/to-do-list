document.addEventListener('DOMContentLoaded', () => {
    const todoForm = document.getElementById('add-todo-form');
    const todoList = document.querySelector('.list-group');
    const emptyState = document.querySelector('.empty-state');

    todoForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const priority = document.getElementById('priority').value;
        const dueDate = document.getElementById('due-date').value;

        await addTodo({ title, description, priority, dueDate });
        todoForm.reset();
        fetchTodos();
    });

    const fetchTodos = async () => {
        const todos = await getTodos();
        renderTodos(todos);
    };

    const renderTodos = (todos) => {
        todoList.innerHTML = '';
        if (todos.length === 0) {
            emptyState.classList.remove('d-none');
        } else {
            emptyState.classList.add('d-none');
            todos.forEach(todo => {
                const li = document.createElement('li');
                li.className = 'list-group-item';
                li.innerHTML = `<span>${todo.title}</span> <button class='btn btn-danger btn-sm' onclick='deleteTodo(${todo.id})'>Delete</button>`;
                todoList.appendChild(li);
            });
        }
    };

    fetchTodos();
});