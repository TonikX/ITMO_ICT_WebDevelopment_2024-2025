import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ConcertCard from '../components/ConcertCard';

const HomePage = () => {
  const [concerts, setConcerts] = useState([]);

  useEffect(() => {
    const fetchConcerts = async () => {
      try {
        const response = await axios.get('http://localhost:8000/concerts/');
        setConcerts(response.data);
      } catch (error) {
        console.error('Error fetching concerts', error);
      }
    };
    fetchConcerts();
  }, []);

  const upcomingConcerts = concerts.filter(concert => concert.status === 'prepared');
  const pastConcerts = concerts.filter(concert => concert.status === 'held');

  return (
    <div>
      <main className="container mt-4">
        <h2 className="mt-5 mb-3">Предстоящие концерты</h2>
        <div className="row gx-4 mt-2">
          {upcomingConcerts.map(concert => (
              <div className="col-md-4 col-sm-6 mb-4" key={concert.id}>
                <ConcertCard concert={concert}/>
              </div>
          ))}
        </div>

        <h2 className="mt-5 mb-3">Прошедшие концерты</h2>
        <div className="row gx-4 mt-2">
          {pastConcerts.map(concert => (
              <div className="col-md-4 col-sm-6 mb-4" key={concert.id}>
                <ConcertCard concert={concert}/>
              </div>
          ))}
        </div>
      </main>
    </div>
  );
};

export default HomePage;
