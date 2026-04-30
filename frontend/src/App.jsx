import React, { useState } from 'react';
import './App.css';
import TripRegistration from './components/TripRegistration';
import TeacherAccess from './components/TeachAccess';

function App() {
  // State to toggle between the two views
  const [activeTab, setActiveTab] = useState('registration');

  return (
    <div>
      {/* Navigation Bar */}
      <div className="nav-bar">
        <button 
          className={activeTab === 'registration' ? '' : 'inactive'} 
          onClick={() => setActiveTab('registration')}
        >
          Trip Registration
        </button>
        <button 
          className={activeTab === 'access' ? '' : 'inactive'} 
          onClick={() => setActiveTab('access')}
        >
          Teacher Access
        </button>
      </div>

      {/* Conditional Rendering: Show only the selected component */}
      {activeTab === 'registration' && <TripRegistration />}
      {activeTab === 'access' && <TeacherAccess />}
    </div>
  );
}

export default App;