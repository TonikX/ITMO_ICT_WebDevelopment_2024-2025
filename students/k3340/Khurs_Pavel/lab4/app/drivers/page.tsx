'use client';

import React, { useEffect, useState, useCallback } from 'react';

import { AgGridReact } from 'ag-grid-react';
import {
  ClientSideRowModelModule,
  colorSchemeDark,
  PaginationModule,
  ValidationModule,
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
import { themeAlpine } from 'ag-grid-community';
import { title } from '@/components/primitives';

const myTheme = themeAlpine.withPart(colorSchemeDark);

export default function DriversPage() {
  const [drivers, setDrivers] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isError, setIsError] = useState<boolean>(false);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

  // Колонки для AG Grid
  const columnDefs = [
    { headerName: 'ID', field: 'id', width: 70 },
    { headerName: 'Паспорт', field: 'passport_data', flex: 1 },
    { headerName: 'Класс', field: 'driver_class', width: 100 },
    { headerName: 'Стаж', field: 'work_experience', width: 100 },
    { headerName: 'Зарплата', field: 'salary', width: 120 },
    { headerName: 'Дата рождения', field: 'date_of_birth', width: 140 },
  ];

  const fetchDrivers = useCallback(async () => {
    try {
      setIsLoading(true);
      const res = await api.get('/api/drivers/');
      setDrivers(res.data);
      setIsError(false);
    } catch (error) {
      console.error('Ошибка при загрузке водителей:', error);
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDrivers();
  }, [fetchDrivers]);

  // Создание водителя
  const handleCreateDriver = async (formData: FormData) => {
    try {
      const passport_data = formData.get('passport_data') as string;
      const driver_class = formData.get('driver_class') as string;
      const work_experience = Number(formData.get('work_experience'));
      const salary = formData.get('salary') as string;
      const date_of_birth = formData.get('date_of_birth') as string;

      await api.post('/api/drivers/', {
        passport_data,
        driver_class,
        work_experience,
        salary,
        date_of_birth,
      });

      setIsModalOpen(false);
      fetchDrivers();
    } catch (error) {
      console.error('Ошибка при создании водителя:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="p-4">
        <p className="text-sm text-neutral-600">Загрузка списка водителей...</p>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="p-4">
        <h2 className="text-lg text-red-500">Ошибка при загрузке водителей</h2>
        <p>Проверьте соединение с сервером или обновите страницу.</p>
      </div>
    );
  }

  return (
    <div className="flex w-full flex-col items-center gap-4 p-4">
      <h2 className={title()}>Список водителей</h2>
      <p className="text-sm text-neutral-500">
        Здесь вы можете просматривать и при необходимости добавлять водителей.
      </p>

      <Divider />

      <Button
        color="primary"
        onPress={() => setIsModalOpen(true)}
        className="max-w-64">
        Добавить водителя
      </Button>

      <Spacer y={1} />

      <div className="w-full" style={{ width: '100%', height: '500px' }}>
        <AgGridReact
          // Указываем модуль RowModel, иначе будет ошибка #200
          theme={myTheme}
          modules={[
            ClientSideRowModelModule,
            ValidationModule,
            PaginationModule,
          ]}
          // Обязательно rowModelType
          rowModelType="clientSide"
          rowData={drivers}
          columnDefs={columnDefs}
          paginationPageSizeSelector={[20, 50, 100]}
          pagination={true}
          paginationPageSize={20}
        />
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
        <ModalContent>
          <ModalHeader>
            <p className="font-semibold">Добавление нового водителя</p>
          </ModalHeader>
          <ModalBody>
            <Form
              className="flex flex-col gap-3"
              action={(formData) => handleCreateDriver(formData)}>
              <Input
                isRequired
                label="Паспорт"
                name="passport_data"
                type="text"
                variant="bordered"
              />
              <Input
                isRequired
                label="Класс (A/B/C)"
                name="driver_class"
                type="text"
                variant="bordered"
              />
              <Input
                isRequired
                label="Стаж (лет)"
                name="work_experience"
                type="number"
                variant="bordered"
              />
              <Input
                isRequired
                label="Зарплата"
                name="salary"
                type="text"
                variant="bordered"
              />
              <Input
                isRequired
                label="Дата рождения"
                name="date_of_birth"
                type="date"
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
