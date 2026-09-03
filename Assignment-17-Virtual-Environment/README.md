## Virtual Environment Creation

To Create a virtual environment:

on Windows::
python -m venv .<env-name>

on Linux/Mac:
python3 -m venv .<env-name>

To activate:
on windows
.<env-name>\Scripts\Activate.ps1

on Linux:
source .<env-name>/bin/activate

To Freeze dependencies:
pip freeze > requirements.txt