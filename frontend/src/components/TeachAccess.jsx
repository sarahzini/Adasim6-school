import React, { useState } from 'react';

function TeacherAccess() {
  const [teacherTz, setTeacherTz] = useState('');
  const [isLogged, setIsLogged] = useState(false);
  const [dataList, setDataList] = useState([]);
  const [message, setMessage] = useState(null);
  
  // Search bar states
  const [searchTeacherId, setSearchTeacherId] = useState('');
  const [searchPupilId, setSearchPupilId] = useState('');

  // Handle Login by calling the backend verify route
  const handleLogin = async (e) => {
    e.preventDefault();
    
    try {
      // Call the login route that uses the verify_teacher in utils.py
      const response = await fetch(`http://localhost:8000/teachers/login/${teacherTz}`);
      const data = await response.json();

      if (response.ok) {
        // Access granted
        setIsLogged(true);
        setMessage(null);
      } else {
        // Access denied 
        setIsLogged(false);
        setMessage(`Auth Error: ${data.detail}`);
      }
    } catch (error) {
      setMessage("Error: Backend connection failed.");
    }
  };

  // Generic function for GET requests
  const fetchData = async (url) => {
    try {
      const response = await fetch(url);
      const data = await response.json();

      if (response.ok) {
        // Ensure data is always an array for the table display
        setDataList(Array.isArray(data) ? data : [data]); 
        setMessage(null);
      } else {
        setDataList([]);
        setMessage(`Error: ${data.detail}`);
      }
    } catch (error) {
      setMessage("Error: Cannot connect to server.");
    }
  };

  // Login view (shown if not logged in)
  if (!isLogged) {
    return (
      <div className="container">
        <h2>Teacher Access</h2>
        <form onSubmit={handleLogin}>
          <label>Enter your Teacher ID (TZ) to access records:</label>
          <input 
            type="text" 
            value={teacherTz} 
            onChange={(e) => setTeacherTz(e.target.value)} 
            required 
          />
          <button type="submit">Access System</button>
        </form>
        {message && <div className="message-box">{message}</div>}
      </div>
    );
  }

  // Dashboard view (shown after successful login)
  return (
    <div className="container">
      <h2>Teacher Dashboard</h2>
      <p>Logged in as: <strong>{teacherTz}</strong></p>

      {/* Main Action Buttons */}
      <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginBottom: '20px' }}>
        <button onClick={() => fetchData(`http://localhost:8000/pupils/?requester_tz=${teacherTz}`)}>
          Get All Pupils
        </button>
        <button onClick={() => fetchData(`http://localhost:8000/teachers/?requester_tz=${teacherTz}`)}>
          Get All Teachers
        </button>
        <button onClick={() => fetchData(`http://localhost:8000/teachers/${teacherTz}/pupils?requester_tz=${teacherTz}`)}>
          Get My Class Pupils
        </button>
      </div>

      {/* Specific Search: Teacher */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
        <input 
          type="text" 
          placeholder="Search specific Teacher ID" 
          value={searchTeacherId} 
          onChange={(e) => setSearchTeacherId(e.target.value)} 
          style={{ margin: 0, flex: 1 }}
        />
        <button onClick={() => fetchData(`http://localhost:8000/teachers/${searchTeacherId}?requester_tz=${teacherTz}`)}>
          Search Teacher
        </button>
      </div>

      {/* Specific Search: Pupil */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <input 
          type="text" 
          placeholder="Search specific Pupil ID" 
          value={searchPupilId} 
          onChange={(e) => setSearchPupilId(e.target.value)} 
          style={{ margin: 0, flex: 1 }}
        />
        <button onClick={() => fetchData(`http://localhost:8000/pupils/${searchPupilId}?requester_tz=${teacherTz}`)}>
          Search Pupil
        </button>
      </div>

      {message && <div className="message-box">{message}</div>}

      {/* Dynamic Results Table */}
      {dataList.length > 0 && (
        <table>
          <thead>
            <tr>
              {Object.keys(dataList[0]).map(key => (
                <th key={key}>{key}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {dataList.map((item, index) => (
              <tr key={index}>
                {Object.values(item).map((val, i) => (
                  <td key={i}>{val}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default TeacherAccess;