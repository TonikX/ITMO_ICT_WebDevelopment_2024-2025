"use client";

import { TourData } from "@/app/tours/types";
import { Card, CardBody } from "@nextui-org/react";

import NextLink from "next/link";
const TourCard: React.FC<TourData> = ({
  title,
  description,
  paymentConditions,
  id,
}) => {
  return (
    <NextLink href={`/tours/${id}`}>
      <Card className="p-6 shadow-lg rounded-lg" isPressable isHoverable>
        <CardBody className="pb-4 flex-col items-start">
          <h4 className="text-xl font-bold">{title}</h4>
          <p className="text-sm">{description}</p>
          <p className="text-sm mt-5 text-green-300">
            Предоплата {paymentConditions}
          </p>
        </CardBody>
      </Card>
    </NextLink>
  );
};

export default TourCard;
