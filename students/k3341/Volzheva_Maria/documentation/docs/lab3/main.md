# Лабораторная работа 3. Реализация серверной части на django rest. Документирование API

## Описание эндпоинтов

### Individual Clients
1. **Получить список клиентов**
```
GET /clients/
```

2. **Получить информацию о клиенте**
```
GET /clients/{id}/
```

3. **Создать клиента**
```
POST /clients/
```

4. **Обновить клиента**
```
PUT /clients/{id}/
```

5. **Частично обновить клиента**
```
PATCH /clients/{id}/
```

6. **Удалить клиента**
```
DELETE /clients/{id}/
```

### Agents
1. **Получить список агентов**
```
GET /agents/
```

2. **Получить информацию об агенте**
```
GET /agents/{id}/
```

3. **Создать агента**
```
POST /agents/
```

4. **Обновить агента**
```
PUT /agents/{id}/
```

5. **Частично обновить агента**
```
PATCH /agents/{id}/
```

6. **Удалить агента**
```
DELETE /agents/{id}/
```

### Individual Contracts
1. **Получить список индивидуальных контрактов**
```
GET /clients/contracts
```

2. **Получить информацию об индивидуальном контракте**
```
GET /clients/contracts/{id}/
```

3. **Создать индивидуальный контракт**
```
POST /clients/contracts
```

4. **Обновить индивидуальный контракт**
```
PUT /clients/contracts/{id}/
```

5. **Частично обновить индивидуальный контракт**
```
PATCH /clients/contracts/{id}/
```

6. **Удалить индивидуальный контракт**
```
DELETE /clients/contracts/{id}/
```

### Labor Contracts
1. **Получить список трудовых контрактов**
```
GET /agents/contracts/
```

2. **Получить информацию о трудовом контракте**
```
GET /agents/contracts/{id}/
```

3. **Создать трудовой контракт**
```
POST /agents/contracts/
```

4. **Обновить трудовой контракт**
```
PUT /agents/contracts/{id}/
```

5. **Частично обновить трудовой контракт**
```
PATCH /agents/contracts/{id}/
```

6. **Удалить трудовой контракт**
```
DELETE /agents/contracts/{id}/
```

### Organizations
1. **Получить список организаций**
```
GET /organizations/
```

2. **Получить информацию об организации**
```
GET /organizations/{id}/
```

3. **Создать организацию**
```
POST /organizations/
```

4. **Обновить организацию**
```
PUT /organizations/{id}/
```

5. **Частично обновить организацию**
```
PATCH /organizations/{id}/
```

6. **Удалить организацию**
```
DELETE /organizations/{id}/
```

### Collective Contracts
1. **Получить список коллективных контрактов**
```
GET /organizations/contracts/
```

2. **Получить информацию о коллективном контракте**
```
GET /organizations/contracts/{id}/
```

3. **Создать коллективный контракт**
```
POST /organizations/contracts/
```

4. **Обновить коллективный контракт**
```
PUT /organizations/contracts/{id}/
```

5. **Частично обновить коллективный контракт**
```
PATCH /organizations/contracts/{id}/
```

6. **Удалить коллективный контракт**
```
DELETE /organizations/contracts/{id}/
```

### Risk Categories
1. **Получить список категорий рисков**
```
GET /categories/
```

2. **Создать категорию риска**
```
POST /categories/
```

3. **Обновить категорию риска**
```
PUT /categories/{id}/
```

4. **Частично обновить категорию риска**
```
PATCH /categories/{id}/
```

5. **Удалить категорию риска**
```
DELETE /categories/{id}/
```

### Insured Employees
1. **Получить список застрахованных сотрудников**
```
GET /employees/
```

2. **Получить информацию о застрахованном сотруднике**
```
GET /employees/{id}/
```

3. **Создать застрахованного сотрудника**
```
POST /employees/
```

4. **Обновить застрахованного сотрудника**
```
PUT /employees/{id}/
```

5. **Частично обновить застрахованного сотрудника**
```
PATCH /employees/{id}/
```

6. **Удалить застрахованного сотрудника**
```
DELETE /employees/{id}/
```

### Insured Events
1. **Получить список событий застрахованных сотрудников**
```
GET /employees/events/
```

2. **Создать событие застрахованного сотрудника**
```
POST /employees/events/
```

### Payments
1. **Получить список выплат застрахованных сотрудников**
```
GET /employees/payments/
```

2. **Создать выплату застрахованного сотрудника**
```
POST /employees/payments/
```

### Other
1. **Получить статистику по контрактам агентов**
```
GET /agents/contracts/stats/
```

2. **Получить информацию о связанных организациях**
```
GET /organizations/related/
```

3. **Получить отчёт по контрактам**
```
GET /report/
```

4. **Получить общую сумму выплат по типам договоров**
```
GET /payments/total
```



### Auth
1. **Получить токен юзера по паролю и никнейму**
```
POST /auth/token/login
```
2. **Вывести информацию о пользователе**
```
GET /auth/users/me
```
3. **Зарегистрировать пользователя**
```
POST /auth/users
```
