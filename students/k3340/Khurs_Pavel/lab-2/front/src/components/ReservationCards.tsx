/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/ban-ts-comment */
"use client";

import { reservationsService } from "@/services/reservationService";
import { Card, CardBody } from "@nextui-org/react";
import { useEffect, useState } from "react";

const ReservationCards = () => {
  const [reservationData, setReservationData] = useState(null);

  useEffect(() => {
    const getData = async () => {
      const reservations = await reservationsService.getAllReservations();
      setReservationData(reservations);
    };
    getData();
  }, []);

  if (!reservationData) {
    return null;
  }
  return (
    <div className="flex flex-wrap container mx-auto gap-8">
      {(reservationData as []).map((item: any) => {
        console.log(item);

        return (
          <Card
            key={item.id}
            className="p-6 shadow-lg rounded-lg"
            isPressable
            isHoverable
          >
            <CardBody className="pb-4 flex-col items-start">
              <h4 className="text-xl font-bold">{item.tour.title}</h4>
              <h2 className="text-xl font-bold">Заявка номер {item.id}</h2>

              <p className="text-sm">{item.tour.description}</p>
              <p className="text-sm mt-5 text-green-300">
                Статус {item.status}
              </p>
            </CardBody>
          </Card>
        );
      })}
    </div>
  );
};

export default ReservationCards;
