const BASE_URL = 'http://localhost:8000/manage';

export const fetchRoutes = async () => {
  try {
    const response = await fetch(`${BASE_URL}/routes`);
    if (!response.ok) {
      throw new Error('Ошибка при загрузке списка маршрутов');
    }
    return await response.json();
  } catch (error) {
    console.error('Ошибка при вызове API fetchRoutes:', error);
    throw error;
  }
};

export const addRoute = async (newRoute) => {
  try {
    const response = await fetch(`${BASE_URL}/add-route`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newRoute),
    });
    if (!response.ok) {
      throw new Error('Ошибка при добавлении маршрута');
    }
    return await response.json();
  } catch (error) {
    console.error('Ошибка при вызове API addRoute:', error);
    throw error;
  }
};

export const deleteRoute = async (route_number) => {
  try {
    const response = await fetch(`${BASE_URL}/delete-route/${route_number}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Ошибка при удалении маршрута');
    }
    return true;
  } catch (error) {
    console.error('Ошибка при вызове API deleteRoute:', error);
    throw error;
  }
};

export const updateRoute = async (route_number, updatedRoute) => {
  try {
    const response = await fetch(`${BASE_URL}/routes/${route_number}/update/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updatedRoute),
    });
    if (!response.ok) {
      throw new Error('Ошибка при обновлении маршрута');
    }
    return await response.json();
  } catch (error) {
    console.error('Ошибка при вызове API updateRoute:', error);
    throw error;
  }
};

export const fetchRoute = async (route_number) => {
  try {
    const response = await fetch(`${BASE_URL}/routes/${route_number}`);
    if (!response.ok) {
      throw new Error('Ошибка при загрузке данных маршрута');
    }
    return await response.json();
  } catch (error) {
    console.error('Ошибка при вызове API fetchRoute:', error);
    throw error;
  }
};
