import { useState } from 'react';
import SIPCalculator from './components/SIPCalculator/SIPCalculator';
import MoneyJourney from './components/MoneyJourney/MoneyJourney';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('sip');

  return (
    <div className="App">
      <div className="app-container">
        <header className="app-header">
          <h1>Money Planner</h1>
        </header>

        <div className="tab-navigation">
          <button
            className={`tab-button ${activeTab === 'sip' ? 'active' : ''}`}
            onClick={() => setActiveTab('sip')}
          >
            Growth Calculator
          </button>
          <button
            className={`tab-button ${activeTab === 'journey' ? 'active' : ''}`}
            onClick={() => setActiveTab('journey')}
          >
            Money Journey
          </button>
        </div>

        {activeTab === 'sip' ? <SIPCalculator /> : <MoneyJourney />}
      </div>
    </div>
  );
}

export default App;
