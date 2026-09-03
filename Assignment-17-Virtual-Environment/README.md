## Virtual Environment Creation

To Create a virtual environment:

on Windows::
python -m venv .<environment-name>

on Linux/Mac:
python3 -m venv .<environment-name>

To activate:
on windows
.<environment-name>\Scripts\Activate.ps1

on Linux:
source .<environment-name>/bin/activate

To Freeze dependencies:
pip freeze > requirements.txt