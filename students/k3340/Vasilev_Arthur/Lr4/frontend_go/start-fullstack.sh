#!/bin/bash

echo "🚀 Starting Printing House Full Stack (Go Backend + Vue Frontend)"
echo ""

# Проверка, что мы в правильной директории
if [ ! -d "../../Lr3/printing_house_go" ]; then
    echo "❌ Error: Run this script from Lr4/frontend_go directory"
    exit 1
fi

# Запуск Go Backend
echo "📦 Step 1/3: Starting Go Backend..."
cd ../../Lr3/printing_house_go
docker-compose down -v 2>/dev/null
docker-compose up -d

echo ""
echo "⏳ Step 2/3: Waiting for backend initialization (15 seconds)..."
sleep 15

# Проверка Backend
echo ""
echo "✅ Step 3/3: Checking backend status..."
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/api/v1/newspapers)

if [ "$BACKEND_STATUS" == "200" ]; then
    echo "✅ Backend is ready! (http://localhost:8080)"
else
    echo "⚠️  Backend returned status: $BACKEND_STATUS"
    echo "   Check logs: cd ../../Lr3/printing_house_go && docker-compose logs app"
fi

# Возвращаемся в frontend_go
cd ../../Lr4/frontend_go

echo ""
echo "📚 Starting Frontend Dev Server..."
echo ""
echo "🎯 URLs:"
echo "  - Frontend: http://localhost:5173"
echo "  - Backend:  http://localhost:8080"
echo ""
echo "👤 Test Users:"
echo "  - Username: admin,  Password: password123"
echo "  - Username: testuser, Password: password123"
echo ""
echo "📖 Press Ctrl+C to stop frontend dev server"
echo "   (Backend will continue running in Docker)"
echo ""

# Запуск Frontend
npm run dev
