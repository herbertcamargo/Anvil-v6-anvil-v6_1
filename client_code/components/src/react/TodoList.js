import React, { useState } from 'react';

const TodoList = () => {
  const [todos, setTodos] = useState([]);
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleAddTodo = () => {
    if (inputValue.trim() !== '') {
      setTodos([...todos, { id: Date.now(), text: inputValue, completed: false }]);
      setInputValue('');
    }
  };

  const handleToggleComplete = (id) => {
    setTodos(
      todos.map(todo => 
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    );
  };

  const handleDeleteTodo = (id) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };

  return (
    <div className="todo-container">
      <h2>React Todo List</h2>
      <div className="input-container">
        <input
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Add a new task"
        />
        <button onClick={handleAddTodo}>Add</button>
      </div>
      <ul className="todo-list">
        {todos.map(todo => (
          <li key={todo.id} className={todo.completed ? 'completed' : ''}>
            <span onClick={() => handleToggleComplete(todo.id)}>
              {todo.text}
            </span>
            <button onClick={() => handleDeleteTodo(todo.id)}>Delete</button>
          </li>
        ))}
      </ul>
      <style jsx>{`
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
          background-color: #4CAF50;
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
      `}</style>
    </div>
  );
};

export default TodoList; 