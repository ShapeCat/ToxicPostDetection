@echo off


python -c "import sys; v=sys.version_info; exit(0 if (v.major==3 and v.minor==10 and v.micro>=6) else 1)"
if %errorlevel% neq 0 (
    echo Python 3.10.6 requered
    pause
    exit /b 1
)


python -m venv venv


call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requerments.txt
pip install -e .


python main.py
pause