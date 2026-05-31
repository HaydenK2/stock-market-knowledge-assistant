import React from 'react';
import QASection from './components/QA/QA.jsx';
import './App.css'

function App() {
  return (
      <div className="App">
        <header className="App-header">
          <h1> Chat with Raggy</h1>
        </header>
        
        <main>
          <QASection />
        </main>
      </div>
    );
}

export default App
