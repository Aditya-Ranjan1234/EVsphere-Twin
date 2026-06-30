@echo off
set VENV_DIR=venv
IF NOT EXIST %VENV_DIR% (
  python -m venv %VENV_DIR%
  echo Virtual environment created in %VENV_DIR%
) ELSE (
  echo Virtual environment already exists.
)
call %VENV_DIR%\Scripts\activate
python -m pip install --upgrade pip
if exist requirements.txt (
  pip install -r requirements.txt
) else (
  echo requirements.txt not found.
)
pause
