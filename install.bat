@echo off
REM Change to script directory
cd /d %~dp0

IF EXIST ".venv\Scripts\activate" (
  echo Activating .venv and installing requirements...
  call .venv\Scripts\activate
  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt
) ELSE (
  echo No .venv found; using system Python to install requirements...
  python -m pip install --upgrade pip || (
    echo Failed to upgrade pip with 'python'; trying 'py -3'...
    py -3 -m pip install --upgrade pip
  )
  python -m pip install -r requirements.txt || py -3 -m pip install -r requirements.txt
)

REM Check tkinter availability
python -c "import tkinter" 2>nul || (
  echo.
  echo WARNING: tkinter is not available in this environment.
  echo - Windows: make sure you installed Python from python.org with Tcl/Tk support.
)
echo All done.
