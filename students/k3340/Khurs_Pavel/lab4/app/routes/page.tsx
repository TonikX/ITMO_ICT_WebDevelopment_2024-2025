'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { AgGridReact } from 'ag-grid-react';
import {
  ClientSideRowModelModule,
  colorSchemeDark,
  PaginationModule,
  ValidationModule,
  themeAlpine,
} from 'ag-grid-community';
import { ColDef } from 'ag-grid-community';
import { api } from '@/api/api';
import { Button } from '@nextui-org/button';
import { Divider } from '@nextui-org/divider';
import { Spacer } from '@nextui-org/spacer';
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
} from '@nextui-org/modal';
import { Input } from '@nextui-org/input';
import { Form } from '@nextui-org/form';
import { title } from '@/components/primitives';

const myTheme = themeAlpine.withPart(colorSchemeDark);

type RouteData = {
  id?: number;
  number: string;
  start_point: string;
  end_point: string;
  operation_start_time: string;
  operation_end_time: string;
  interval: string;
  duration: string;
};

type MyColDef = ColDef<RouteData>;

export default function RoutesPage() {
  const [routes, setRoutes] = useState<RouteData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingRoute, setEditingRoute] = useState<RouteData | null>(null);
  const [intervalHours, setIntervalHours] = useState('');
  const [intervalMinutes, setIntervalMinutes] = useState('');
  const [durationHours, setDurationHours] = useState('');
  const [durationMinutes, setDurationMinutes] = useState('');

  const columnDefs: MyColDef[] = [
    { headerName: 'ID', field: 'id', width: 70 },
    { headerName: 'Номер', field: 'number', flex: 1 },
    { headerName: 'Начальная точка', field: 'start_point', flex: 1 },
    { headerName: 'Конечная точка', field: 'end_point', flex: 1 },
    { headerName: 'Время начала', field: 'operation_start_time', width: 120 },
    { headerName: 'Время конца', field: 'operation_end_time', width: 120 },
    { headerName: 'Интервал', field: 'interval', width: 100 },
    { headerName: 'Длительность', field: 'duration', width: 100 },
  ];

  const fetchRoutes = useCallback(async () => {
    try {
      setIsLoading(true);
      const res = await api.get('/api/routes/');
      setRoutes(res.data);
      setIsError(false);
    } catch (error) {
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchRoutes();
  }, [fetchRoutes]);

  const handleAddRouteClick = () => {
    setEditingRoute(null);
    setIntervalHours('');
    setIntervalMinutes('');
    setDurationHours('');
    setDurationMinutes('');
    setIsModalOpen(true);
  };

  const handleEditRoute = (routeData: RouteData) => {
    setEditingRoute(routeData);
    const [iH, iM] = parseHHMM(routeData.interval);
    setIntervalHours(iH);
    setIntervalMinutes(iM);
    const [dH, dM] = parseHHMM(routeData.duration);
    setDurationHours(dH);
    setDurationMinutes(dM);
    setIsModalOpen(true);
  };

  const parseHHMM = (value: string) => {
    if (!value) return ['00', '00'];
    const parts = value.split(':');
    return [parts[0] || '00', parts[1] || '00'];
  };

  const buildHHMMSS = (h: string, m: string) => {
    const hh = h || '00';
    const mm = m || '00';
    return `${hh.padStart(2, '0')}:${mm.padStart(2, '0')}:00`;
  };

  const handleSubmitRoute = async (formData: FormData) => {
    try {
      const number = formData.get('number') as string;
      const start_point = formData.get('start_point') as string;
      const end_point = formData.get('end_point') as string;
      const operation_start_time = formData.get(
        'operation_start_time',
      ) as string;
      const operation_end_time = formData.get('operation_end_time') as string;
      const intervalStr = buildHHMMSS(intervalHours, intervalMinutes);
      const durationStr = buildHHMMSS(durationHours, durationMinutes);

      if (editingRoute) {
        const routeId = editingRoute.id;
        await api.patch(`/api/routes/${routeId}/`, {
          number,
          start_point,
          end_point,
          operation_start_time: operation_start_time + ':00',
          operation_end_time: operation_end_time + ':00',
          interval: intervalStr,
          duration: durationStr,
        });
      } else {
        await api.post('/api/routes/', {
          number,
          start_point,
          end_point,
          operation_start_time: operation_start_time + ':00',
          operation_end_time: operation_end_time + ':00',
          interval: intervalStr,
          duration: durationStr,
        });
      }

      setIsModalOpen(false);
      fetchRoutes();
    } catch (error) {}
  };

  if (isLoading) {
    return (
      <div className="p-4">
        <p className="text-sm text-neutral-600">Загрузка списка маршрутов...</p>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="p-4">
        <h2 className="text-lg text-red-500">Ошибка при загрузке маршрутов</h2>
        <p>Проверьте соединение с сервером или попробуйте обновить страницу.</p>
      </div>
    );
  }

  const getFieldValue = (fieldName: keyof RouteData, defaultVal = '') => {
    return (
      editingRoute ? editingRoute[fieldName] || defaultVal : defaultVal
    ) as string;
  };

  return (
    <div className="flex w-full flex-col gap-4 p-4">
      <h2 className={title()}>Список маршрутов</h2>
      <p className="text-sm text-neutral-500">
        Здесь вы можете просматривать, добавлять и редактировать маршруты.
      </p>

      <Divider />

      <div className="flex gap-2">
        <Button color="primary" onPress={handleAddRouteClick}>
          Добавить маршрут
        </Button>
      </div>

      <Spacer y={1} />

      <div
        className="ag-theme-alpine"
        style={{ width: '100%', height: '500px' }}>
        <AgGridReact<RouteData>
          theme={myTheme}
          modules={[
            ClientSideRowModelModule,
            ValidationModule,
            PaginationModule,
          ]}
          rowModelType="clientSide"
          columnDefs={columnDefs}
          rowData={routes}
          pagination
          paginationPageSize={20}
          onRowClicked={(params) => handleEditRoute(params.data as RouteData)}
        />
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
        <ModalContent>
          <ModalHeader>
            <p className="font-semibold">
              {editingRoute ? 'Редактировать маршрут' : 'Добавить маршрут'}
            </p>
          </ModalHeader>
          <ModalBody>
            <Form className="flex flex-col gap-3" action={handleSubmitRoute}>
              <Input
                isRequired
                label="Номер"
                name="number"
                type="text"
                variant="bordered"
                defaultValue={getFieldValue('number')}
              />
              <Input
                isRequired
                label="Начальная точка"
                name="start_point"
                type="text"
                variant="bordered"
                defaultValue={getFieldValue('start_point')}
              />
              <Input
                isRequired
                label="Конечная точка"
                name="end_point"
                type="text"
                variant="bordered"
                defaultValue={getFieldValue('end_point')}
              />
              <label className="text-sm font-medium">
                Время начала (HH:MM)
              </label>
              <Input
                isRequired
                name="operation_start_time"
                type="time"
                variant="bordered"
                defaultValue={
                  editingRoute
                    ? getFieldValue('operation_start_time').slice(0, 5)
                    : ''
                }
              />
              <label className="text-sm font-medium">Время конца (HH:MM)</label>
              <Input
                isRequired
                name="operation_end_time"
                type="time"
                variant="bordered"
                defaultValue={
                  editingRoute
                    ? getFieldValue('operation_end_time').slice(0, 5)
                    : ''
                }
              />
              <div className="flex flex-col gap-2">
                <label className="text-sm font-medium">Интервал</label>
                <div className="flex items-center gap-2">
                  <Input
                    label="Часы"
                    name="intervalHours"
                    type="number"
                    step="1"
                    variant="bordered"
                    value={intervalHours}
                    onValueChange={setIntervalHours}
                  />
                  <Input
                    label="Минуты"
                    name="intervalMinutes"
                    type="number"
                    step="1"
                    variant="bordered"
                    value={intervalMinutes}
                    onValueChange={setIntervalMinutes}
                  />
                </div>
              </div>
              <div className="flex flex-col gap-2">
                <label className="text-sm font-medium">Длительность</label>
                <div className="flex items-center gap-2">
                  <Input
                    label="Часы"
                    name="durationHours"
                    type="number"
                    step="1"
                    variant="bordered"
                    value={durationHours}
                    onValueChange={setDurationHours}
                  />
                  <Input
                    label="Минуты"
                    name="durationMinutes"
                    type="number"
                    step="1"
                    variant="bordered"
                    value={durationMinutes}
                    onValueChange={setDurationMinutes}
                  />
                </div>
              </div>
              <Spacer y={0.5} />
              <ModalFooter>
                <Button type="submit" color="primary">
                  Сохранить
                </Button>
                <Button
                  variant="flat"
                  color="default"
                  onPress={() => setIsModalOpen(false)}>
                  Отмена
                </Button>
              </ModalFooter>
            </Form>
          </ModalBody>
        </ModalContent>
      </Modal>
    </div>
  );
}
