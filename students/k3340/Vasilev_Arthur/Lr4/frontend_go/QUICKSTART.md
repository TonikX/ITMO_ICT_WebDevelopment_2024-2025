# 🚀 Quick Start Guide

## Запуск полного стека (Backend + Frontend)

### Windows

```bash
cd Lr4/frontend_go
start-fullstack.bat
```

### Linux/Mac

```bash
cd Lr4/frontend_go
chmod +x start-fullstack.sh
./start-fullstack.sh
```

Скрипт автоматически:
1. ✅ Запустит Go backend в Docker
2. ⏳ Подождёт инициализации БД (15 сек)
3. ✅ Проверит статус backend
4. 🎨 Запустит frontend dev server

## URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8080/api/v1

## Тестовые пользователи

| Username | Password |
|----------|----------|
| admin | password123 |
| testuser | password123 |

## Ручной запуск (если нужно)

### 1. Backend

```bash
cd Lr3/printing_house_go
docker-compose up -d
```

### 2. Frontend

```bash
cd Lr4/frontend_go
npm install  # первый раз
npm run dev
```

## Остановка

**Frontend**: Нажать `Ctrl+C` в терминале

**Backend**:
```bash
cd Lr3/printing_house_go
docker-compose down
```

## Проверка работы

```bash
# Backend
curl http://localhost:8080/api/v1/newspapers

# Frontend
# Открыть в браузере: http://localhost:5173
```

## Troubleshooting

### Backend не запустился

```bash
cd Lr3/printing_house_go
docker-compose logs app
```

### Frontend показывает Network Error

1. Проверить, что backend запущен: `docker-compose ps`
2. Проверить URL в `src/services/api.ts`
3. Перезапустить backend: `docker-compose restart app`

---

Полная документация: [README.md](README.md)
