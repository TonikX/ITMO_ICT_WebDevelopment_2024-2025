# Отчет по лабораторной работе

## Введение
Проект представляет собой клиентскую часть системы управления аэропортом, разработанную с использованием Vue.js и Vuetify. Система обеспечивает интерфейс для управления сотрудниками, рейсами и другими аспектами работы аэропорта.

## Технологический стек
- Vue.js 3
- Vuetify 3
- Axios
- JWT Authentication


## Структура приложения
```vue
airport_vue/
├── src/
│   ├── components/         # Переиспользуемые компоненты
│   ├── store/              # Состояние приложения
│   ├── plugins/            # Плагины Vue
│   ├── views/             # Компоненты-страницы
│   ├── router/            # Настройки маршрутизации
│   └── App.vue            # Корневой компонент
│   └── main.js            # Точка входа
```
## Система аутентификации
- Использование JWT токенов
- Хранение в localStorage
- Автоматическое обновление токенов
- Защита маршрутов


## Основные компоненты

### LoginView
Компонент авторизации:
- Валидация данных
- Отправка запроса на сервер
- Обработка ошибок

### HeaderButtons
Компонент навигации, отвечающий за:
- Отображение меню
- Кнопки навигации
- Выход из системы

### TokenRefresh
Автоматическое обновление JWT токенов:
- Отслеживание срока действия
- Запрос новых токенов
- Обработка ошибок авторизации

### ProfileView
Управление профилем пользователя:
- Редактирование личных данных
- Загрузка аватара
- Обновление информации о сотруднике

### EmployeeList
Список сотрудников:
- Фильтрация
- Поиск
- Отображение информации о сотруднике
- Добавление
- Удаление

### EmployeeDetail
Детальная информация о сотруднике:
- Просмотр данных
- Управление статусом (найм/увольнение)
- Обновление информации

### EmployeeAdd
Форма добавления нового сотрудника:
- Валидация данных
- Отправка данных на сервер
- Уведомление об успешном добавлении

### Остальные компоненты на основе моделей устроены аналогичным образом

## Взаимодействие с бэкендом

### Авторизация и аутентификация

```javascript
// Вход в систему
async login(username, password) {
  const response = await axios.post('/api/auth/login/', {
    username: username,
    password: password
  })
  return response.data // Получаем access и refresh токены
}
```

### Управление профилем

```javascript 
// Получение данных профиля
async fetchEmployeeProfile() {
  const tokens = JSON.parse(localStorage.getItem('tokens'))
  const userResponse = await axios.get('/api/auth/users/me/', {
    headers: { Authorization: `Bearer ${tokens.access}` }
  })
  const employeeResponse = await axios.get(`/api/employee/${userResponse.data.id}/`)
  return employeeResponse.data
}

// Обновление аватара
async updateAvatar(avatar) {
  const formData = new FormData()
  formData.append('avatar', avatar)
  await axios.patch(`/api/user/${userId}/avatar/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}
```

### Управление сотрудниками

```javascript 
// Получение списка сотрудников
async getEmployees() {
  const response = await axios.get('/api/employee/')
  return response.data
}

// Обновление данных сотрудника
async updateEmployee(id, data) {
  await axios.patch(`/api/employee/${id}/`, data)
}

// Увольнение/найм сотрудника
async changeEmployeeStatus(id, isActive) {
  await axios.patch(`/api/employee/${id}/`, {
    user: {
      is_active: isActive,
      password: isActive ? DEFAULT_PASSWORD : FIRED_PASSWORD
    }
  })
}
```

### Обработка ошибок

```javascript 
try {
  await api.call()
} catch (error) {
  if (error.response) {
    // Обработка ошибок сервера (4xx, 5xx)
    console.error('Server error:', error.response.data)
  } else if (error.request) {
    // Ошибка сети
    console.error('Network error:', error.request) 
  } else {
    // Другие ошибки
    console.error('Error:', error.message)
  }
}
```

### Автоматическое обновление токена

```javascript 
// Перехватчик для обновления токена
axios.interceptors.response.use(
  response => response,
  async error => {
    if (error.response.status === 401) {
      const tokens = JSON.parse(localStorage.getItem('tokens'))
      const newTokens = await refreshToken(tokens.refresh)
      localStorage.setItem('tokens', JSON.stringify(newTokens))
      error.config.headers['Authorization'] = `Bearer ${newTokens.access}`
      return axios(error.config)
    }
    return Promise.reject(error)
  }
)
```

### Конфигурация Axios

```javascript
// Базовая конфигурация
axios.defaults.baseURL = 'http://127.0.0.1:8000'

// Добавление токена к каждому запросу
axios.interceptors.request.use(config => {
  const tokens = JSON.parse(localStorage.getItem('tokens'))
  if (tokens) {
    config.headers.Authorization = `Bearer ${tokens.access}`
  }
  return config
})
```

## Заключение

В ходе выполнения лабораторной работы был успешно разработан фронтенд для системы управления аэропортом с использованием современного стека технологий Vue.js и Vuetify.

### Основные достижения:

- Реализована система аутентификации с использованием JWT токенов
- Создан удобный интерфейс управления профилями сотрудников
- Внедрена система разграничения прав доступа (админ/сотрудник)
- Налажено эффективное взаимодействие с REST API бэкенда

Проект демонстрирует практическое применение современных веб-технологий и паттернов разработки. Созданный интерфейс обеспечивает удобное управление данными и предоставляет необходимый функционал для различных категорий пользователей.

Разработанное решение может служить основой для дальнейшего расширения функциональности системы управления аэропортом.