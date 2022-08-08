# Project Name
* ArchiveLog - version 1.1.30

Project date: from April to June/2022


## Additional infromation
- Icon from: https://icon-icons.com/icon/file-archive/193973
- Not commercial used.

- This project will save me a lot of time at work because my services generate 70 GB of logs per month, and the law requires log archiving for +/- 20 years.
- I wrote this program after my job, because it is an element of my self-development.
- If you find a bug you can write to me :)


## Table of Contents
* [General Info](#general-information)
* [Additional infromation](#additional-infromation)
* [General Information](#general-information)
* [Technologies Used](#technologies-used)
* [Usage](#usage)
* [Project Status](#project-status)
* [Contact](#contact)
<!-- * [License](#license) -->


## General Information
The program has:
- Getting params from configuration file
- Securing password in configuration file
- Archived application (or IIS) log to zip
- Export archives log to FTP
- Delete source logs from directory
- Delete archives files (with time shift)
- Sending E-Mail after error 


## Technologies Used
- Python - version 3.10.1
  - SMTPLib
- ConfigParser (pycparser) - version 2.21
- ConfigUpdater - version 3.1
- Cryptography - version 37.0.2
- PyInstaller - version 5.1

<!--
## Features
None


## Screenshots
![Example screenshot](./img/screenshot.png)


## Setup
What are the project requirements/dependencies? Where are they listed? A requirements.txt or a Pipfile.lock file perhaps? Where is it located?

Proceed to describe how to install / setup one's local environment / get started with the project.
-->

## Usage
If you would like to run from script:
1. Run main.py
2. Complete config.ini
3. Run main.py
4. Look at the log file

If u would like to run EXE (and then example put it into Task Scheduler, like me):

Generate EXE file - CMD ->
```batch
pip install pyinstaller --proxy http://user:pass@proxy.pl:3128
cd Building
pyinstaller ArchiveLog.spec
```

1. Run .\dist\ArchiveLog.exe
2. Complete config.ini
3. Run again ArchiveLog.exe
4. Look at the log file


## Project Status
Project is: _in QA testing_

<!-- _complete_ / _no longer being worked on_ (and why) -->

<!--
## Room for Improvement
No plans
-->

## Contact
Created by [@Majster](mailto:rachuna.mikolaj@gmail.com)
