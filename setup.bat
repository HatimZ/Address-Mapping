@echo off

:: Create necessary directories
mkdir logs 2>nul

:: Setup frontend
echo Setting up frontend...
cd front-end
call npm install
call npm run build
cd ..

:: Setup backend
echo Setting up backend...
python -m venv venv
call venv\Scripts\activate
pip install -r back-end\requirements.txt

:: Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    (
        echo NODE_ENV=development
        echo PYTHONUNBUFFERED=1
    ) > .env
)

echo Setup completed successfully! 