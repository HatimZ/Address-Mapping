@echo off

REM Check Python version
python --version 2>NUL | findstr /C:"Python 3.12" >NUL
if errorlevel 1 (
    echo Error: Python 3.12 is required
    python --version
    exit /b 1
)

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
python -m pip install --upgrade pip
pip install -r requirements\base.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    echo MONGODB_URL=mongodb://localhost:27017> .env
    echo MONGODB_USERNAME=hatimzahid1995>> .env
    echo MONGODB_PASSWORD=zD3KvZ7quY2xf77t>> .env
    echo MONGODB_DATABASE=address_distance>> .env
    echo NOMINATIM_BASE_URL=https://nominatim.openstreetmap.org>> .env
    echo NOMINATIM_USER_AGENT=AddressDistanceAPI/1.0>> .env
)

REM Run the application
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000 