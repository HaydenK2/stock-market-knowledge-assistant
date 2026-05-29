import React from 'react';
import ItemList from './components/Items.jsx';
import './App.css'

function App() {
  return (
      <div className="App">
        <header className="App-header">
          <h1>Item Management App</h1>
        </header>
        <main>
          <ItemList />
        </main>
      </div>
    );
}

export default App
