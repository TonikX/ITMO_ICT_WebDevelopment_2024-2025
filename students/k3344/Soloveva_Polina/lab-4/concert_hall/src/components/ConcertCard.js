import { formatInTimeZone } from 'date-fns-tz';
import { ru } from 'date-fns/locale';

const ConcertCard = ({ concert }) => {
  const { title, date, time, image, id } = concert;

  const timeZone = 'Europe/Moscow';

  const dateObj = new Date(date);
  const timeObj = new Date(`${date}T${time}`);

  const formattedDate = formatInTimeZone(dateObj, timeZone, "d MMMM", { locale: ru });
  const formattedTime = formatInTimeZone(timeObj, timeZone, "HH:mm", { locale: ru });

  return (
    <a href={`/concerts/${id}`} className="card mb-4 text-decoration-none" style={{ width: '20rem', cursor: 'pointer', color: 'inherit' }}>
      <img
        src={image}
        className="card-img-top"
        alt={title}
        style={{ width: '100%', height: '200px', objectFit: 'cover' }}
      />
      <div className="card-body">
        <h5 className="card-title">{title}</h5>
        <p className="card-text"><small>{formattedDate}, {formattedTime}</small></p>
      </div>
    </a>
  );
};

export default ConcertCard;
