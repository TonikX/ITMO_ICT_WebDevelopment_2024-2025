"use client";
import { useEffect, useState } from "react";
import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
} from "@nextui-org/react";

interface SalesData {
  country: string;
  sales: number;
}

export default function SalesByCountry() {
  const [salesData, setSalesData] = useState<SalesData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSalesData = async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/statistics/sales-by-country`
        );
        if (!response.ok) {
          throw new Error("Failed to load data");
        }
        const data: SalesData[] = await response.json();
        setSalesData(data);
        setLoading(false);
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
      } catch (err) {
        setError("Не удалось загрузить данные");
        setLoading(false);
      }
    };

    fetchSalesData();
  }, []);

  if (loading) return <div className="text-center text-lg">Загрузка...</div>;
  if (error) return <div className="text-center text-red-500">{error}</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4 text-center">
        Проданные туры по странам
      </h1>
      <Table aria-label="Проданные туры по странам" isStriped>
        <TableHeader>
          <TableColumn>Страна</TableColumn>
          <TableColumn>Продажи</TableColumn>
        </TableHeader>
        <TableBody>
          {salesData.map((data, index) => (
            <TableRow key={index}>
              <TableCell>{data.country}</TableCell>
              <TableCell>{data.sales}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
