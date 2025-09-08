@echo off

REM Create virtual environment
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

echo Virtual environment is ready.
echo To activate it, run: venv\Scripts\activate
pause
