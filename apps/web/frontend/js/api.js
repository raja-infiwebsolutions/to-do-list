const API_URL = 'http://localhost:8000/api/todos';

async function getTodos() {
    const response = await fetch(API_URL);
    return await response.json();
}

async function addTodo(todo) {
    await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(todo)
    });
}

async function deleteTodo(id) {
    await fetch(`${API_URL}/${id}`, {
        method: 'DELETE'
    });
}