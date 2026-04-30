import React, { useState } from 'react';

function TripRegistration() {
  // States for the form
  const [role, setRole] = useState('pupils'); // Default to pupil
  const [id, setId] = useState('');
  const [fullName, setFullName] = useState('');
  const [classNum, setClassNum] = useState('');
  
  // State for feedback messages
  const [message, setMessage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent page reload

    // --- FRONTEND VALIDATION ---
    // 1. Check ID: Only numbers, between 8 and 10 digits
    const idRegex = /^[0-9]{8,10}$/;
    if (!idRegex.test(id)) {
      setMessage("Error: ID must contain only numbers and be between 8 and 10 digits.");
      return; // Stop the function here, don't send to backend
    }

    // 2. Check Name: Only letters and spaces
    const nameRegex = /^[a-zA-Z\s]+$/;
    if (!nameRegex.test(fullName)) {
      setMessage("Error: Full Name must contain only letters and spaces.");
      return; // Stop the function here
    }
    // ---------------------------
    
    // Prepare the data matching the backend schemas
    const payload = role === 'pupils' 
      ? { PupilID: id, PupilFullName: fullName, PupilClass: parseInt(classNum) }
      : { TeacherID: id, TeacherFullName: fullName, TeacherClass: parseInt(classNum) };

    try {
      // Send the POST request
      const response = await fetch(`http://localhost:8000/${role}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`Success: ${data.message}`);
        // Clear the form
        setId(''); setFullName(''); setClassNum('');
      } else {
        // Show the backend error (e.g., the "tiyoul" message or validation error)
        setMessage(`Error: ${data.detail}`);
      }
    } catch (error) {
      setMessage("Error: Cannot connect to the server.");
    }
  };

  return (
    <div className="container">
      <h2>Trip Registration</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="radio-group">
          <label>
            <input 
              type="radio" 
              value="pupils" 
              checked={role === 'pupils'} 
              onChange={() => setRole('pupils')} 
            />
            I am a Pupil
          </label>
          <label style={{ marginLeft: '20px' }}>
            <input 
              type="radio" 
              value="teachers" 
              checked={role === 'teachers'} 
              onChange={() => setRole('teachers')} 
            />
            I am a Teacher
          </label>
        </div>

        <label>ID Number (8-10 digits)</label>
        <input 
          type="text" 
          value={id} 
          onChange={(e) => setId(e.target.value)} 
          required 
        />

        <label>Full Name (Letters only)</label>
        <input 
          type="text" 
          value={fullName} 
          onChange={(e) => setFullName(e.target.value)} 
          required 
        />

        <label>Class Number</label>
        <input 
          type="number" 
          value={classNum} 
          onChange={(e) => setClassNum(e.target.value)} 
          required 
        />

        <button type="submit">Register for the trip</button>
      </form>

      {/* Show message if exists */}
      {message && <div className="message-box">{message}</div>}
    </div>
  );
}

export default TripRegistration;