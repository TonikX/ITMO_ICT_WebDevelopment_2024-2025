const BASE_URL = 'http://localhost:8000/manage';

export const fetchDrivers = async () => {
  try {
    const response = await fetch(`${BASE_URL}/drivers`);
    if (!response.ok) {
      throw new Error('Ошибка при загрузке списка водителей');
    }
    return await response.json();
  } catch (error) {
    console.error('Ошибка при вызове API fetchDrivers:', error);
    throw error;
  }
};

export const addDriver = async (newDriver) => {
  try {
    const response = await fetch(`${BASE_URL}/drivers/create/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newDriver),
    });
    if (!response.ok) {
      throw new Error('Ошибка при добавлении водителя');
    }
    return await response.json();
  } catch (error) {
    console.error('Ошибка при вызове API addDriver:', error);
    throw error;
  }
};

export const deleteDriver = async (passport_number) => {
  try {
    const response = await fetch(`${BASE_URL}/drivers/${passport_number}/delete/`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Ошибка при удалении водителя');
    }
    return true;
  } catch (error) {
    console.error('Ошибка при вызове API deleteDriver:', error);
    throw error;
  }
};

export const updateDriver = async (passport_number, updatedDriver) => {
  try {
    const response = await fetch(`${BASE_URL}/drivers/${passport_number}/update/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updatedDriver),
    });
    if (!response.ok) {
      throw new Error('Ошибка при обновлении данных водителя');
    }
    return await response.json();
  } catch (error) {
    console.error('Ошибка при вызове API updateDriver:', error);
    throw error;
  }
};
