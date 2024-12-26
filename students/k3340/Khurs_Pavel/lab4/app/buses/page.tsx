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

export default function BusesPage() {
  const [buses, setBuses] = useState<any[]>([]);
  const [busTypes, setBusTypes] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);

  const [isBusModalOpen, setIsBusModalOpen] = useState(false);
  const [isBusTypeModalOpen, setIsBusTypeModalOpen] = useState(false);

  const [editingBus, setEditingBus] = useState<any | null>(null);
  const [isEditBusModalOpen, setIsEditBusModalOpen] = useState(false);

  const [editingBusType, setEditingBusType] = useState<any | null>(null);
  const [isEditBusTypeModalOpen, setIsEditBusTypeModalOpen] = useState(false);

  const columnDefs = [
    { headerName: 'ID', field: 'id', width: 70 },
    {
      headerName: 'Рег. номер',
      field: 'registration_number',
      flex: 1,
    },
    {
      headerName: 'Тип автобуса',
      field: 'bus_type.name',
      flex: 1,
    },
    {
      headerName: 'В эксплуатации?',
      field: 'in_service',
      width: 150,
    },
  ];

  const fetchBuses = useCallback(async () => {
    try {
      setIsLoading(true);
      const res = await api.get('/api/buses/');
      setBuses(res.data);
      setIsError(false);
    } catch (error) {
      console.error('Ошибка при загрузке автобусов:', error);
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchBusTypes = useCallback(async () => {
    try {
      const res = await api.get('/api/bus-types/');
      setBusTypes(res.data);
    } catch (error) {
      console.error('Ошибка при загрузке типов автобусов:', error);
    }
  }, []);

  useEffect(() => {
    fetchBuses();
    fetchBusTypes();
  }, [fetchBuses, fetchBusTypes]);

  const handleCreateBus = async (formData: FormData) => {
    try {
      const registration_number = formData.get('registration_number') as string;
      const in_serviceRaw = formData.get('in_service') as string;
      const in_service = in_serviceRaw === 'true';
      const bus_type_id = Number(formData.get('bus_type_id'));

      await api.post('/api/buses/', {
        registration_number,
        in_service,
        bus_type_id,
      });

      setIsBusModalOpen(false);
      fetchBuses();
    } catch (error) {
      console.error('Ошибка при создании автобуса:', error);
    }
  };

  const handleCreateBusType = async (formData: FormData) => {
    try {
      const name = formData.get('name') as string;
      const capacity = Number(formData.get('capacity'));

      await api.post('/api/bus-types/', {
        name,
        capacity,
      });

      setIsBusTypeModalOpen(false);
      fetchBusTypes();
    } catch (error) {
      console.error('Ошибка при создании типа автобуса:', error);
    }
  };

  // Triggered when a row cell is clicked
  // If it's bus_type.name => edit BusType, otherwise edit Bus
  const handleCellClick = (params: any) => {
    if (params.colDef.field === 'bus_type.name') {
      if (!params.data.bus_type) return;
      setEditingBusType(params.data.bus_type);
      setIsEditBusTypeModalOpen(true);
    } else {
      setEditingBus(params.data);
      setIsEditBusModalOpen(true);
    }
  };

  const handleEditBus = async (formData: FormData) => {
    if (!editingBus) return;
    try {
      const registration_number = formData.get('registration_number') as string;
      const in_serviceRaw = formData.get('in_service') as string;
      const in_service = in_serviceRaw === 'true';
      const bus_type_id = Number(formData.get('bus_type_id'));

      await api.patch(`/api/buses/${editingBus.id}/`, {
        registration_number,
        in_service,
        bus_type_id,
      });

      setIsEditBusModalOpen(false);
      setEditingBus(null);
      fetchBuses();
    } catch (error) {
      console.error('Ошибка при редактировании автобуса:', error);
    }
  };

  const handleEditBusType = async (formData: FormData) => {
    if (!editingBusType) return;
    try {
      const name = formData.get('name') as string;
      const capacity = Number(formData.get('capacity'));

      await api.patch(`/api/bus-types/${editingBusType.id}/`, {
        name,
        capacity,
      });

      setIsEditBusTypeModalOpen(false);
      setEditingBusType(null);
      fetchBusTypes();
      fetchBuses();
    } catch (error) {
      console.error('Ошибка при редактировании типа автобуса:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="p-4">
        <p className="text-sm text-neutral-600">Загрузка списка автобусов...</p>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="p-4">
        <h2 className="text-lg text-red-500">Ошибка при загрузке автобусов</h2>
        <p>Проверьте соединение с сервером или обновите страницу.</p>
      </div>
    );
  }

  const getBusField = (fieldName: string) => {
    return editingBus ? editingBus[fieldName] : '';
  };

  const getBusTypeField = (fieldName: string) => {
    return editingBusType ? editingBusType[fieldName] : '';
  };

  return (
    <div className="flex w-full flex-col items-center gap-4 p-4">
      <h2 className={title()}>Список автобусов</h2>
      <p className="text-sm text-neutral-500">
        Клик по ячейке «Тип автобуса» для изменения его полей, или по другим
        ячейкам для редактирования самого автобуса.
      </p>

      <Divider />

      <div className="flex gap-2">
        <Button
          color="primary"
          onPress={() => setIsBusModalOpen(true)}
          className="max-w-64">
          Добавить автобус
        </Button>
        <Button
          color="secondary"
          onPress={() => setIsBusTypeModalOpen(true)}
          className="max-w-64">
          Добавить тип автобуса
        </Button>
      </div>

      <Spacer y={1} />

      <div className="w-full" style={{ width: '100%', height: '500px' }}>
        <AgGridReact
          theme={myTheme}
          modules={[
            ClientSideRowModelModule,
            ValidationModule,
            PaginationModule,
          ]}
          rowModelType="clientSide"
          columnDefs={columnDefs}
          rowData={buses}
          pagination
          paginationPageSize={20}
          paginationPageSizeSelector={[20, 50, 100]}
          onCellClicked={handleCellClick}
        />
      </div>

      <Modal isOpen={isBusModalOpen} onClose={() => setIsBusModalOpen(false)}>
        <ModalContent>
          <ModalHeader>
            <p className="font-semibold">Добавление нового автобуса</p>
          </ModalHeader>
          <ModalBody>
            <Form
              className="flex flex-col gap-3"
              action={(formData) => handleCreateBus(formData)}>
              <Input
                isRequired
                label="Рег. номер"
                name="registration_number"
                type="text"
                variant="bordered"
              />
              <div>
                <p className="mb-1 text-sm">В эксплуатации?</p>
                <select
                  name="in_service"
                  className="w-full rounded-md border border-default-300 p-2 text-sm"
                  defaultValue="true"
                  required>
                  <option value="true">Да</option>
                  <option value="false">Нет</option>
                </select>
              </div>
              <div>
                <p className="mb-1 text-sm">Тип автобуса</p>
                <select
                  name="bus_type_id"
                  className="w-full rounded-md border border-default-300 p-2 text-sm"
                  required>
                  <option value="">-- Выберите тип --</option>
                  {busTypes.map((type) => (
                    <option key={type.id} value={type.id}>
                      {type.name} (Capacity: {type.capacity})
                    </option>
                  ))}
                </select>
              </div>
              <Spacer y={0.5} />
              <ModalFooter>
                <Button type="submit" color="primary">
                  Сохранить
                </Button>
                <Button
                  variant="flat"
                  color="default"
                  onPress={() => setIsBusModalOpen(false)}>
                  Отмена
                </Button>
              </ModalFooter>
            </Form>
          </ModalBody>
        </ModalContent>
      </Modal>

      <Modal
        isOpen={isBusTypeModalOpen}
        onClose={() => setIsBusTypeModalOpen(false)}>
        <ModalContent>
          <ModalHeader>
            <p className="font-semibold">Добавление нового типа автобуса</p>
          </ModalHeader>
          <ModalBody>
            <Form
              className="flex flex-col gap-3"
              action={(formData) => handleCreateBusType(formData)}>
              <Input
                isRequired
                label="Название типа"
                name="name"
                type="text"
                variant="bordered"
              />
              <Input
                isRequired
                label="Вместимость"
                name="capacity"
                type="number"
                variant="bordered"
              />
              <Spacer y={0.5} />
              <ModalFooter>
                <Button type="submit" color="primary">
                  Сохранить
                </Button>
                <Button
                  variant="flat"
                  color="default"
                  onPress={() => setIsBusTypeModalOpen(false)}>
                  Отмена
                </Button>
              </ModalFooter>
            </Form>
          </ModalBody>
        </ModalContent>
      </Modal>

      <Modal
        isOpen={isEditBusModalOpen}
        onClose={() => setIsEditBusModalOpen(false)}>
        <ModalContent>
          <ModalHeader>
            <p className="font-semibold">Редактирование автобуса</p>
          </ModalHeader>
          <ModalBody>
            <Form
              className="flex flex-col gap-3"
              action={(formData) => handleEditBus(formData)}>
              <Input
                isRequired
                label="Рег. номер"
                name="registration_number"
                type="text"
                variant="bordered"
                defaultValue={getBusField('registration_number')}
              />
              <div>
                <p className="mb-1 text-sm">В эксплуатации?</p>
                <select
                  name="in_service"
                  className="w-full rounded-md border border-default-300 p-2 text-sm"
                  required
                  defaultValue={editingBus?.in_service ? 'true' : 'false'}>
                  <option value="true">Да</option>
                  <option value="false">Нет</option>
                </select>
              </div>
              <div>
                <p className="mb-1 text-sm">Тип автобуса</p>
                <select
                  name="bus_type_id"
                  className="w-full rounded-md border border-default-300 p-2 text-sm"
                  required
                  defaultValue={
                    editingBus?.bus_type?.id ? editingBus.bus_type.id : ''
                  }>
                  <option value="">-- Выберите тип --</option>
                  {busTypes.map((type) => (
                    <option key={type.id} value={type.id}>
                      {type.name} (Capacity: {type.capacity})
                    </option>
                  ))}
                </select>
              </div>
              <Spacer y={0.5} />
              <ModalFooter>
                <Button type="submit" color="primary">
                  Сохранить
                </Button>
                <Button
                  variant="flat"
                  color="default"
                  onPress={() => setIsEditBusModalOpen(false)}>
                  Отмена
                </Button>
              </ModalFooter>
            </Form>
          </ModalBody>
        </ModalContent>
      </Modal>

      <Modal
        isOpen={isEditBusTypeModalOpen}
        onClose={() => setIsEditBusTypeModalOpen(false)}>
        <ModalContent>
          <ModalHeader>
            <p className="font-semibold">Редактирование типа автобуса</p>
          </ModalHeader>
          <ModalBody>
            <Form
              className="flex flex-col gap-3"
              action={(formData) => handleEditBusType(formData)}>
              <Input
                isRequired
                label="Название типа"
                name="name"
                type="text"
                variant="bordered"
                defaultValue={getBusTypeField('name')}
              />
              <Input
                isRequired
                label="Вместимость"
                name="capacity"
                type="number"
                variant="bordered"
                defaultValue={getBusTypeField('capacity')}
              />
              <Spacer y={0.5} />
              <ModalFooter>
                <Button type="submit" color="primary">
                  Сохранить
                </Button>
                <Button
                  variant="flat"
                  color="default"
                  onPress={() => setIsEditBusTypeModalOpen(false)}>
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
