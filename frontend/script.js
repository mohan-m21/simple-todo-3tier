const API_URL = 'http://localhost:5000/api/todos';  // will be proxied or direct in prod

async function fetchTodos() {
  try {
    const res = await fetch(API_URL);
    const todos = await res.json();
    const list = document.getElementById('todoList');
    list.innerHTML = '';
    todos.forEach(todo => {
      const li = document.createElement('li');
      li.innerHTML = `
        <span class="${todo.completed ? 'completed' : ''}">${todo.task}</span>
        <button onclick="toggleTodo(${todo.id}, ${!todo.completed})">
          ${todo.completed ? 'Undo' : 'Complete'}
        </button>
      `;
      list.appendChild(li);
    });
  } catch (err) {
    console.error('Error fetching todos:', err);
  }
}

async function addTodo() {
  const input = document.getElementById('taskInput');
  const task = input.value.trim();
  if (!task) return;

  try {
    await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task })
    });
    input.value = '';
    fetchTodos();
  } catch (err) {
    console.error('Error adding todo:', err);
  }
}

async function toggleTodo(id, completed) {
  try {
    await fetch(`${API_URL}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ completed })
    });
    fetchTodos();
  } catch (err) {
    console.error('Error updating todo:', err);
  }
}

// Load todos on page load
fetchTodos();
