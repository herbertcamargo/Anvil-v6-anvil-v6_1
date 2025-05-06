<template>
  <div class="todo-container">
    <h2>Vue Todo List</h2>
    <div class="input-container">
      <input 
        type="text" 
        v-model="newTodo" 
        @keyup.enter="addTodo"
        placeholder="Add a new task"
      />
      <button @click="addTodo">Add</button>
    </div>
    <ul class="todo-list">
      <li 
        v-for="todo in todos" 
        :key="todo.id" 
        :class="{ completed: todo.completed }"
      >
        <span @click="toggleComplete(todo)">{{ todo.text }}</span>
        <button @click="deleteTodo(todo)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'TodoList',
  data() {
    return {
      todos: [],
      newTodo: ''
    };
  },
  methods: {
    addTodo() {
      if (this.newTodo.trim()) {
        this.todos.push({
          id: Date.now(),
          text: this.newTodo,
          completed: false
        });
        this.newTodo = '';
      }
    },
    toggleComplete(todo) {
      todo.completed = !todo.completed;
    },
    deleteTodo(todo) {
      this.todos = this.todos.filter(t => t.id !== todo.id);
    }
  }
};
</script>

<style scoped>
.todo-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}
.input-container {
  display: flex;
  margin-bottom: 20px;
}
input {
  flex-grow: 1;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
}
button {
  padding: 10px 15px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 1px solid #eee;
}
li.completed span {
  text-decoration: line-through;
  color: #888;
}
li button {
  background-color: #f44336;
  padding: 5px 10px;
  border-radius: 4px;
}
</style> 