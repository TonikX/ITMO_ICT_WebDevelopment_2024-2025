import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { formatInTimeZone } from 'date-fns-tz';
import { ru } from 'date-fns/locale';

const ConcertDetail = () => {
  const { id } = useParams();
  const [concert, setConcert] = useState(null);

  useEffect(() => {
    const fetchConcert = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/concerts/${id}/`);
        setConcert(response.data);
      } catch (error) {
        console.error('Error fetching concert details', error);
      }
    };
    fetchConcert();
  }, [id]);

  if (!concert) return <div>Loading...</div>;

  const timeZone = 'Europe/Moscow';
  const dateObj = new Date(concert.date);
  const timeObj = new Date(`${concert.date}T${concert.time}`);
  const formattedDate = formatInTimeZone(dateObj, timeZone, "d MMMM", { locale: ru });
  const formattedTime = formatInTimeZone(timeObj, timeZone, "HH:mm", { locale: ru });
 console.log(concert.tickets)
  return (
    <div className="container mt-4">
      <img
        src={concert.image}
        className="card-img-top"
        alt={concert.title}
        style={{ width: '100%', height: '300px', objectFit: 'cover' }}
      />
      <h1 className="mt-2">{concert.title}</h1>
      <p>{formattedDate}, {formattedTime} • {concert.age_limit}+</p>
      <p>{concert.description}</p>

      {concert.status !== 'held' && (
        concert.tickets?.length > 0 ? (
            <div>
                <h3>Доступные билеты</h3>
                <div style={{overflowX: 'auto', whiteSpace: 'nowrap', paddingBottom: '10px'}}>
                    <div className="d-flex mt-2" style={{gap: '10px', flexWrap: 'nowrap'}}>
                        {concert.tickets.map(ticket => (
                            <div className="card" key={ticket.id} style={{width: '300px', flex: '0 0 auto'}}>
                                <div className="card-body">
                                    <h5 className="card-title">{ticket.name}</h5>
                                    <p className="card-text"><strong>Цена:</strong> {ticket.price} ₽</p>
                                    <p className="card-text"><strong>Осталось
                                        билетов:</strong> {ticket.available_quantity}</p>
                                    <a href={`/orders/${ticket.id}`} className="btn btn-primary">Купить билет</a>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        ) : (
            <p>Билеты недоступны для этого концерта.</p>
        )
      )}
    </div>
  );
};

export default ConcertDetail;
