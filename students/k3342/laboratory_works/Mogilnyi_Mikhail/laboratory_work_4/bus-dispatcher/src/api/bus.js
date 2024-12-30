const BASE_URL = 'http://localhost:8000/manage';

export const fetchBuses = async () => {
  try {
    const response = await fetch(`${BASE_URL}/buses`);
    if (!response.ok) {
      throw new Error('Ошибка при загрузке списка автобусов');
    }
    return await response.json();
  } catch (error) {
    console.error('Ошибка при вызове API fetchBuses:', error);
    throw error;
  }
};

export const fetchBus = async (registration_number) => {
  try {
    const response = await fetch(`${BASE_URL}/bus/${registration_number}`);
    if (!response.ok) {
      throw new Error('Ошибка при загрузке данных автобуса');
    }
    return await response.json(); // Возвращаем объект с данными автобуса
  } catch (error) {
    console.error('Ошибка при вызове API fetchBus:', error);
    throw error;
  }
};

// Обновление данных автобуса
export const updateBus = async (bus) => {
  try {
    const response = await fetch(`${BASE_URL}/bus/${bus.registration_number}/update/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(bus),
    });
    if (!response.ok) {
      throw new Error('Ошибка при обновлении автобуса');
    }
    return await response.json(); // Возвращаем обновленный автобус
  } catch (error) {
    console.error('Ошибка при вызове API updateBus:', error);
    throw error;
  }
};

export const addBus = async (newBus) => {
  try {
    const response = await fetch(`${BASE_URL}/add-bus/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newBus),
    });
    if (!response.ok) {
      throw new Error('Ошибка при добавлении автобуса');
    }
    return await response.json();
  } catch (error) {
    console.error('Ошибка при вызове API addBus:', error);
    throw error;
  }
};

export const deleteBus = async (registration_number) => {
  try {
    const response = await fetch(`${BASE_URL}/delete-bus/${registration_number}/`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Ошибка при удалении автобуса');
    }
    return true;
  } catch (error) {
    console.error('Ошибка при вызове API deleteBus:', error);
    throw error;
  }
};
