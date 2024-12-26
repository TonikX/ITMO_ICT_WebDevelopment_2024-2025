'use client';

import React, { useEffect, useState } from 'react';
import { Card, CardHeader, CardBody } from '@nextui-org/card';
import { Spacer } from '@nextui-org/spacer';
import { Divider } from '@nextui-org/divider';
import { api } from '@/api/api';
import { title } from '@/components/primitives';

// Recharts imports
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
} from 'recharts';

export default function DashboardPage() {
  const [driversCount, setDriversCount] = useState<number | null>(null);
  const [activeBusesCount, setActiveBusesCount] = useState<number | null>(null);
  const [inActiveBusesCount, setInActiveBusesCount] = useState<number | null>(
    null,
  );
  const [totalRoutesCount, setTotalRoutesCount] = useState<number | null>(null);
  const [shiftsTodayCount, setShiftsTodayCount] = useState<number | null>(null);
  const [problemNotifications, setProblemNotifications] = useState<string[]>(
    [],
  );
  const [isError, setIsError] = useState<boolean>(false);

  useEffect(() => {
    async function fetchData() {
      try {
        const driversRes = await api.get(`/api/drivers/`);
        const driversData = driversRes.data;
        setDriversCount(Array.isArray(driversData) ? driversData.length : 0);

        const busesRes = await api.get(`/api/buses/`);
        const busesData = busesRes.data;
        if (Array.isArray(busesData)) {
          const activeCount = busesData.filter(
            (bus: any) => bus.in_service,
          ).length;
          setActiveBusesCount(activeCount);
          setInActiveBusesCount(busesData.length - activeCount);
        }

        const routesRes = await api.get(`/api/routes/`);
        const routesData = routesRes.data;
        setTotalRoutesCount(Array.isArray(routesData) ? routesData.length : 0);

        const workShiftsRes = await api.get(`/api/work-shifts/`);
        const workShiftsData = workShiftsRes.data;

        if (Array.isArray(workShiftsData)) {
          const today = new Date().toISOString().split('T')[0];
          const shiftsToday = workShiftsData.filter(
            (shift: any) => shift.date === today,
          );
          setShiftsTodayCount(shiftsToday.length);

          const problemStatuses = [
            'Breakdown',
            'No Driver',
            'No Bus',
            'Sick',
            'Absent',
          ];
          const problemShifts = workShiftsData.filter((shift: any) =>
            problemStatuses.includes(shift.status),
          );
          const notifications = problemShifts.map((shift: any) => {
            return `Смена #${shift.id}: статус «${shift.status}»${
              shift.reason ? ` — ${shift.reason}` : ''
            }`;
          });
          setProblemNotifications(notifications);
        }
      } catch (error) {
        console.error('Ошибка при загрузке данных:', error);
        setIsError(true);
      }
    }

    fetchData();
  }, []);

  if (isError) {
    return (
      <div className="flex flex-col items-center justify-center p-4">
        <h2 className="text-lg text-red-500">Ошибка при загрузке данных</h2>
        <p>Проверьте соединение с сервером.</p>
      </div>
    );
  }

  // Prepare data for Recharts
  const busPieData = [
    { name: 'Активные', value: activeBusesCount || 0 },
    { name: 'Не активные', value: inActiveBusesCount || 0 },
  ];

  const barData = [
    { name: 'Водители', count: driversCount || 0 },
    {
      name: 'Автобусы',
      count: (activeBusesCount || 0) + (inActiveBusesCount || 0),
    },
    { name: 'Маршруты', count: totalRoutesCount || 0 },
    { name: 'Смены (сегодня)', count: shiftsTodayCount || 0 },
  ];

  return (
    <div className="flex flex-col gap-4 p-4">
      <h1 className={title()}>Панель управления автопарком</h1>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="pb-0">
            <p className="font-semibold">Водители</p>
          </CardHeader>
          <CardBody>
            <p className="text-lg font-bold">
              {driversCount !== null ? driversCount : '...'}
            </p>
          </CardBody>
        </Card>

        <Card>
          <CardHeader className="pb-0">
            <p className="font-semibold">Активные автобусы</p>
          </CardHeader>
          <CardBody>
            <p className="text-lg font-bold">
              {activeBusesCount !== null ? activeBusesCount : '...'}
            </p>
          </CardBody>
        </Card>
        <Card>
          <CardHeader className="pb-0">
            <p className="font-semibold">Не активные автобусы</p>
          </CardHeader>
          <CardBody>
            <p className="text-lg font-bold">
              {inActiveBusesCount !== null ? inActiveBusesCount : '...'}
            </p>
          </CardBody>
        </Card>
        <Card>
          <CardHeader className="pb-0">
            <p className="font-semibold">Маршруты</p>
          </CardHeader>
          <CardBody>
            <p className="text-lg font-bold">
              {totalRoutesCount !== null ? totalRoutesCount : '...'}
            </p>
          </CardBody>
        </Card>

        <Card>
          <CardHeader className="pb-0">
            <p className="font-semibold">Смены на сегодня</p>
          </CardHeader>
          <CardBody>
            <p className="text-lg font-bold">
              {shiftsTodayCount !== null ? shiftsTodayCount : '...'}
            </p>
          </CardBody>
        </Card>
      </div>

      <Divider />

      <Card>
        <CardHeader>
          <p className="font-semibold">Проблемные смены</p>
        </CardHeader>
        <CardBody className="flex flex-col gap-2">
          {problemNotifications.length > 0 ? (
            problemNotifications.map((msg, idx) => (
              <p key={idx} className="text-sm text-red-600">
                {msg}
              </p>
            ))
          ) : (
            <p className="text-sm text-neutral-400">Нет текущих проблем</p>
          )}
        </CardBody>
      </Card>

      <Spacer y={1} />

      {/* Example Charts */}
      <div className="grid gap-8 md:grid-cols-2">
        <div className="flex flex-col items-center">
          <p className="mb-2 text-sm font-bold">
            Активные / Неактивные автобусы
          </p>
          <PieChart width={300} height={300}>
            <Pie
              data={busPieData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={100}>
              <Cell fill="#00C49F" />
              <Cell fill="#FF8042" />
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </div>

        <div className="flex flex-col items-center">
          <p className="mb-2 text-sm font-bold">Обзор ключевых показателей</p>
          <ResponsiveContainer width="95%" height={300}>
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#8884d8" barSize={40} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <Spacer y={2} />
    </div>
  );
}
