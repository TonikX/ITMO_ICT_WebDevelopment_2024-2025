import React, { useEffect, useState } from 'react';

const Cabinets = () => {
    const [cabinets, setCabinets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchCabinets = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/cabinets/');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setCabinets(data);
            } catch (err) {
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        fetchCabinets();
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    return (
        <div>
            <h1>Cabinets</h1>
            <ul>
                {cabinets.map(cabinet => (
                    <li key={cabinet.id}>{cabinet.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default Cabinets;
