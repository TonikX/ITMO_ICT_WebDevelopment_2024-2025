@echo off
echo 🚀 Starting Printing House Full Stack (Go Backend + Vue Frontend)
echo.

REM Check if we're in the right directory
if not exist "..\..\Lr3\printing_house_go\" (
    echo ❌ Error: Run this script from Lr4\frontend_go directory
    exit /b 1
)

REM Start Go Backend
echo 📦 Step 1/3: Starting Go Backend...
cd ..\..\Lr3\printing_house_go
docker-compose down -v >nul 2>&1
docker-compose up -d

echo.
echo ⏳ Step 2/3: Waiting for backend initialization (15 seconds)...
timeout /t 15 /nobreak >nul

REM Check Backend
echo.
echo ✅ Step 3/3: Checking backend status...
curl -s -o nul -w "%%{http_code}" http://localhost:8080/api/v1/newspapers > temp_status.txt
set /p BACKEND_STATUS=<temp_status.txt
del temp_status.txt

if "%BACKEND_STATUS%"=="200" (
    echo ✅ Backend is ready! (http://localhost:8080^)
) else (
    echo ⚠️  Backend returned status: %BACKEND_STATUS%
    echo    Check logs: cd ..\..\Lr3\printing_house_go ^&^& docker-compose logs app
)

REM Return to frontend_go
cd ..\..\Lr4\frontend_go

echo.
echo 📚 Starting Frontend Dev Server...
echo.
echo 🎯 URLs:
echo   - Frontend: http://localhost:5173
echo   - Backend:  http://localhost:8080
echo.
echo 👤 Test Users:
echo   - Username: admin,  Password: password123
echo   - Username: testuser, Password: password123
echo.
echo 📖 Press Ctrl+C to stop frontend dev server
echo    (Backend will continue running in Docker^)
echo.

REM Start Frontend
npm run dev
