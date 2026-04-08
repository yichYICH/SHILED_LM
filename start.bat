@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo    IP Shield - 知识产权主动防护平台
echo ========================================

REM 检查环�?echo 检查环�?..
where python >nul 2>nul
if errorlevel 1 (
    echo 错误: 未找�?Python
    pause
    exit /b 1
)

where node >nul 2>nul
if errorlevel 1 (
    echo 错误: 未找�?Node.js
    pause
    exit /b 1
)

where npm >nul 2>nul
if errorlevel 1 (
    echo 错误: 未找�?npm
    pause
    exit /b 1
)

REM 获取项目目录
set "SCRIPT_DIR=%~dp0"
set "BACKEND_DIR=%SCRIPT_DIR%backend"
set "FRONTEND_DIR=%SCRIPT_DIR%frontend"

echo 项目目录: %SCRIPT_DIR%

REM 启动后端
echo 启动后端服务...
cd /d "%BACKEND_DIR%"

REM 检查并创建虚拟环境
if not exist "venv" (
    echo 创建Python虚拟环境...
    python -m venv venv
)

REM 激活虚拟环�?if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM 安装依赖
echo 安装后端依赖...
pip install -r requirements.txt >nul 2>&1

REM 启动后端服务（新窗口�?start "IP Shield Backend" cmd /k "python main.py"

REM 等待后端启动
timeout /t 3 /nobreak >nul

REM 启动前端
echo 启动前端服务...
cd /d "%FRONTEND_DIR%"

REM 安装依赖
echo 安装前端依赖...
call npm install --silent

REM 启动前端服务（新窗口�?start "IP Shield Frontend" cmd /k "npm run dev"

REM 显示访问信息
echo.
echo ========================================
echo           服务启动完成�?echo ========================================
echo 前端界面: http://127.0.0.1:5173
echo 后端API:  http://127.0.0.1:8000
echo API文档: http://127.0.0.1:8000/docs
echo.
echo 请勿关闭此窗口，关闭所有cmd窗口以停止服�?echo ========================================
echo.
pause
