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

export default function WorkShiftsPage() {
  const [workShifts, setWorkShifts] = useState<any[]>([]);
  const [drivers, setDrivers] = useState<any[]>([]);
  const [buses, setBuses] = useState<any[]>([]);
  const [routes, setRoutes] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [editingShift, setEditingShift] = useState<any | null>(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  const columnDefs = [
    { headerName: 'ID', field: 'id', width: 70 },
    { headerName: 'Дата', field: 'date', width: 120 },
    {
      headerName: 'Начало смены',
      field: 'shift_start_time',
      width: 120,
    },
    {
      headerName: 'Конец смены',
      field: 'shift_end_time',
      width: 120,
    },
    {
      headerName: 'Водитель',
      field: 'driver.passport_data',
      flex: 1,
    },
    {
      headerName: 'Автобус',
      field: 'bus.registration_number',
      flex: 1,
    },
    {
      headerName: 'Маршрут',
      field: 'route.number',
      flex: 1,
    },
    {
      headerName: 'Статус',
      field: 'status',
      width: 150,
    },
  ];

  const fetchData = useCallback(async () => {
    try {
      setIsLoading(true);

      // 1) Load WorkShifts
      const resWorkShifts = await api.get('/api/work-shifts/');
      setWorkShifts(resWorkShifts.data);

      // 2) Load Drivers
      const resDrivers = await api.get('/api/drivers/');
      setDrivers(resDrivers.data);

      // 3) Load Buses
      const resBuses = await api.get('/api/buses/');
      setBuses(resBuses.data);

      // 4) Load Routes
      const resRoutes = await api.get('/api/routes/');
      setRoutes(resRoutes.data);

      setIsError(false);
    } catch (error) {
      console.error('Ошибка при загрузке смен:', error);
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleCreateShift = async (formData: FormData) => {
    try {
      const driver_id = Number(formData.get('driver_id'));
      const bus_id = Number(formData.get('bus_id'));
      const route_id = Number(formData.get('route_id'));
      const date = formData.get('date') as string;
      const shift_start_time = formData.get('shift_start_time') as string;
      const shift_end_time = formData.get('shift_end_time') as string;
      const status = formData.get('status') as string;
      const reason = formData.get('reason') as string;

      await api.post('/api/work-shifts/', {
        driver_id,
        bus_id,
        route_id,
        date,
        shift_start_time,
        shift_end_time,
        status,
        reason,
      });

      setIsCreateModalOpen(false);
      fetchData();
    } catch (error) {
      console.error('Ошибка при создании смены:', error);
    }
  };

  const handleEditShift = async (formData: FormData) => {
    if (!editingShift) return;

    try {
      const driver_id = Number(formData.get('driver_id'));
      const bus_id = Number(formData.get('bus_id'));
      const route_id = Number(formData.get('route_id'));
      const date = formData.get('date') as string;
      const shift_start_time = formData.get('shift_start_time') as string;
      const shift_end_time = formData.get('shift_end_time') as string;
      const status = formData.get('status') as string;
      const reason = formData.get('reason') as string;

      await api.patch(`/api/work-shifts/${editingShift.id}/`, {
        driver_id,
        bus_id,
        route_id,
        date,
        shift_start_time,
        shift_end_time,
        status,
        reason,
      });

      setIsEditModalOpen(false);
      setEditingShift(null);
      fetchData();
    } catch (error) {
      console.error('Ошибка при редактировании смены:', error);
    }
  };

  const handleRowClick = (params: any) => {
    setEditingShift(params.data);
    setIsEditModalOpen(true);
  };

  if (isLoading) {
    return (
      <div className="p-4">
        <p className="text-sm text-neutral-600">Загрузка списка смен...</p>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="p-4">
        <h2 className="text-lg text-red-500">Ошибка при загрузке смен</h2>
        <p>Проверьте соединение с сервером или попробуйте обновить страницу.</p>
      </div>
    );
  }

  const getFieldValue = (field: string) =>
    editingShift ? editingShift[field] || '' : '';

  const getFkId = (fkObj: any) => (fkObj ? fkObj.id : '');

  return (
    <div className="flex flex-col gap-4 p-4">
      <h2 className={title()}>Список смен</h2>
      <p className="text-sm text-neutral-500">
        Здесь вы можете просматривать, добавлять и редактировать смены.
      </p>

      <Divider />

      <Button color="primary" onPress={() => setIsCreateModalOpen(true)}>
        Добавить смену
      </Button>

      <Spacer y={1} />

      <div
        className="ag-theme-alpine"
        style={{ width: '100%', height: '500px' }}>
        <AgGridReact
          theme={myTheme}
          modules={[
            ClientSideRowModelModule,
            ValidationModule,
            PaginationModule,
          ]}
          rowModelType="clientSide"
          columnDefs={columnDefs}
          rowData={workShifts}
          pagination
          paginationPageSize={10}
          onRowClicked={handleRowClick}
        />
      </div>

      <Modal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}>
        <ModalContent>
          <ModalHeader>
            <p className="font-semibold">Добавить смену</p>
          </ModalHeader>
          <ModalBody>
            <Form
              className="flex flex-col gap-3"
              action={(formData) => handleCreateShift(formData)}>
              <div>
                <p className="mb-1 text-sm">Водитель</p>
                <select
                  name="driver_id"
                  className="w-full rounded-md border p-2 text-sm"
                  required>
                  <option value="">-- Выберите водителя --</option>
                  {drivers.map((d) => (
                    <option key={d.id} value={d.id}>
                      {d.passport_data}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <p className="mb-1 text-sm">Автобус</p>
                <select
                  name="bus_id"
                  className="w-full rounded-md border p-2 text-sm"
                  required>
                  <option value="">-- Выберите автобус --</option>
                  {buses.map((b) => (
                    <option key={b.id} value={b.id}>
                      {b.registration_number}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <p className="mb-1 text-sm">Маршрут</p>
                <select
                  name="route_id"
                  className="w-full rounded-md border p-2 text-sm"
                  required>
                  <option value="">-- Выберите маршрут --</option>
                  {routes.map((r) => (
                    <option key={r.id} value={r.id}>
                      {r.number}
                    </option>
                  ))}
                </select>
              </div>

              <Input
                isRequired
                label="Дата"
                name="date"
                type="date"
                variant="bordered"
              />

              <Input
                isRequired
                label="Начало (HH:MM:SS)"
                name="shift_start_time"
                type="text"
                variant="bordered"
                placeholder="08:00:00"
              />

              <Input
                isRequired
                label="Конец (HH:MM:SS)"
                name="shift_end_time"
                type="text"
                variant="bordered"
                placeholder="16:00:00"
              />

              <div>
                <p className="mb-1 text-sm">Статус</p>
                <select
                  name="status"
                  className="w-full rounded-md border p-2 text-sm"
                  required
                  defaultValue="Worked">
                  <option value="Worked">Worked</option>
                  <option value="Absent">Absent</option>
                  <option value="Sick">Sick</option>
                  <option value="Breakdown">Breakdown</option>
                  <option value="No Driver">No Driver</option>
                  <option value="No Bus">No Bus</option>
                </select>
              </div>

              <Input
                label="Причина"
                name="reason"
                type="text"
                variant="bordered"
                placeholder="Если не Worked"
              />

              <Spacer y={0.5} />
              <ModalFooter>
                <Button type="submit" color="primary">
                  Сохранить
                </Button>
                <Button
                  variant="flat"
                  color="default"
                  onPress={() => setIsCreateModalOpen(false)}>
                  Отмена
                </Button>
              </ModalFooter>
            </Form>
          </ModalBody>
        </ModalContent>
      </Modal>

      <Modal
        isOpen={isEditModalOpen}
        onClose={() => {
          setIsEditModalOpen(false);
          setEditingShift(null);
        }}>
        <ModalContent>
          <ModalHeader>
            <p className="font-semibold">Редактировать смену</p>
          </ModalHeader>
          <ModalBody>
            <Form
              className="flex flex-col gap-3"
              action={(formData) => handleEditShift(formData)}>
              <div>
                <p className="mb-1 text-sm">Водитель</p>
                <select
                  name="driver_id"
                  className="w-full rounded-md border p-2 text-sm"
                  required
                  defaultValue={editingShift?.driver?.id || ''}>
                  <option value="">-- Выберите водителя --</option>
                  {drivers.map((d) => (
                    <option key={d.id} value={d.id}>
                      {d.passport_data}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <p className="mb-1 text-sm">Автобус</p>
                <select
                  name="bus_id"
                  className="w-full rounded-md border p-2 text-sm"
                  required
                  defaultValue={editingShift?.bus?.id || ''}>
                  <option value="">-- Выберите автобус --</option>
                  {buses.map((b) => (
                    <option key={b.id} value={b.id}>
                      {b.registration_number}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <p className="mb-1 text-sm">Маршрут</p>
                <select
                  name="route_id"
                  className="w-full rounded-md border p-2 text-sm"
                  required
                  defaultValue={editingShift?.route?.id || ''}>
                  <option value="">-- Выберите маршрут --</option>
                  {routes.map((r) => (
                    <option key={r.id} value={r.id}>
                      {r.number}
                    </option>
                  ))}
                </select>
              </div>

              <Input
                isRequired
                label="Дата"
                name="date"
                type="date"
                variant="bordered"
                defaultValue={getFieldValue('date')}
              />

              <Input
                isRequired
                label="Начало (HH:MM:SS)"
                name="shift_start_time"
                type="text"
                variant="bordered"
                defaultValue={getFieldValue('shift_start_time')}
              />

              <Input
                isRequired
                label="Конец (HH:MM:SS)"
                name="shift_end_time"
                type="text"
                variant="bordered"
                defaultValue={getFieldValue('shift_end_time')}
              />

              <div>
                <p className="mb-1 text-sm">Статус</p>
                <select
                  name="status"
                  className="w-full rounded-md border p-2 text-sm"
                  required
                  defaultValue={getFieldValue('status')}>
                  <option value="Worked">Worked</option>
                  <option value="Absent">Absent</option>
                  <option value="Sick">Sick</option>
                  <option value="Breakdown">Breakdown</option>
                  <option value="No Driver">No Driver</option>
                  <option value="No Bus">No Bus</option>
                </select>
              </div>

              <Input
                label="Причина"
                name="reason"
                type="text"
                variant="bordered"
                defaultValue={getFieldValue('reason')}
              />

              <Spacer y={0.5} />
              <ModalFooter>
                <Button type="submit" color="primary">
                  Сохранить
                </Button>
                <Button
                  variant="flat"
                  color="default"
                  onPress={() => {
                    setIsEditModalOpen(false);
                    setEditingShift(null);
                  }}>
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
