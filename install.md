## Installation Guide

## Prerequisites
Before you begin, ensure you have met the following requirements:

- **Operating System:** Windows, macOS, Linux
- **Web Browser:** A modern web browser (e.g., Google Chrome, Mozilla Firefox, Safari)

***Install Python***:
1) Download the windows installer for the python version you desire from [Python Downloads](https://www.python.org/downloads/) Based on the Operating System of your PC, you can download and install Python's latest as well as older versions. Please find below instructions for the same based on your OS.
2) Double-click on the downloaded file and follow the instructions as requested.
3) Once completed, add python in the environment variables of your system settings to enable python compiling from your command line.
4) You can verify if the Python installation is successful either through the command line or through the IDLE app that gets installed along with the installation. Search for the command prompt and type “python”. You can see that Python "version" is successfully installed.

  To check python version, run this command in your CMD or Terminal:
  
  ```bash
  python --version
  ```

## Follow these steps to install the project:

### Installing (for Windows)

1. Clone the Repository
Start by cloning the repository to your local machine. 

``` bash
git clone https://github.com/Fall-2024-SE-Group/campus-job-review-system.git
```

```
cd campus-job-review-system/
```
```
python -m venv venv
```
```
.\venv\Scripts\activate
```
```
pip install --upgrade pip
```
```
pip install -r requirements.txt
```
```
set FLASK_APP=crudapp.py
```
```
flask db init
```
```
flask db migrate -m "entries table"
```
```
flask db upgrade
```
```
flask run
```


### Mac OS

MacOS comes with Python pre-installed. But it's Python Version 2.7, which is now deprecated (abandoned by the Python developer community).

To install the latest version of python in your mac, first you need to install [Homebrew](https://brew.sh/), a powerful package manager for Mac.

Open your terminal and run this command to install Homebrew in your system:
```bash
"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Your terminal will ask for admin.user access of your system. You will need to type your password to run this command. This is the same password you type when you log into your Mac. Type it and hit enter.

Once you are done with installing the Homebrew package, you can run this command in your terminal to install python with the desired version you want.

```bash
python version 3.6.5
```
Once done, you can run this command to check if you have successfully installed python in your system or its version:
```bash
python3 --version
```

## Maintaining Database file

To create/add new tables, run the following commands before starting the server:
```bash
flask shell
from app import db
db.create_all()
````

To delete all the tables, run following commands before starting the server:
```bash
flask shell
from app import db
db.drop_all()
```

