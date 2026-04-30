import React, { useState, useEffect } from 'react';

function LiveTracking() {
    const [locations, setLocations] = useState([]);
    const [time, setTime] = useState(new Date().toLocaleTimeString());

    // Digital Clock that Updates every second
    useEffect(() => {
        const timer = setInterval(() => {
            setTime(new Date().toLocaleTimeString());
        }, 1000);
        return () => clearInterval(timer);
    }, []);

    // Data Refresh that Updates every minute
    const refreshData = async () => {
        await fetch('http://localhost:8000/location/run-simulation'); //move people
        const res = await fetch('http://localhost:8000/location/'); //get uptaded locations
        const data = await res.json();
        setLocations(data);
    };

    useEffect(() => {
        refreshData();
        const interval = setInterval(refreshData, 60000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="container">
            <p style={{ textAlign: 'right', fontWeight: 'bold', color: '#2c3e50' }}>
                System Time: {time}
            </p>
            <h2>Live Tracking Dashboard</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Latitude</th>
                        <th>Longitude</th>
                    </tr>
                </thead>
                <tbody>
                    {locations.map((loc) => (
                        <tr key={loc.id}>
                            <td><strong>{loc.id}</strong></td>
                            <td>{loc.latitude}</td>
                            <td>{loc.longitude}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default LiveTracking;