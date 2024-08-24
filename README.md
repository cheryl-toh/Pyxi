# Desk Companion Robot

Welcome to the Desk Companion Robot project! This intelligent, pet-like robot assistant is designed to enhance your desktop experience by automating tasks, managing schedules, and providing companionship.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Installation](#installation)
3. [Usage](#usage)

## Project Overview

Deployment: https://cheryl-toh.github.io/Pyxi/

Phase 1 Run Through: https://www.youtube.com/watch?v=vKJkiZ0tka0

## Key Features

- **Voice and Facial Animation**
  - Wake Word Detection: "Hello, Pyxi!"
  - Speech Recognition for seamless interaction
- **Task Management**
  - To-Do List: Add, remove, and send to-do items
  - Calendar Events: Manage your schedule with voice commands
  - Clock feature: Time and Timer
  - Weather feature: Weather and Temepature
- **Desktop Automation**
  - Open Applications: Voice commands to open apps like Notepad, Google Chrome
  - Spotify Control: Play your favorite songs with simple voice commands
  - Power Settings: Control your computer's power settings


## Installation

To get started with the Desk Companion Robot, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/cheryl-toh/pyxi.git
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    - enter your gmail address in the Email service
    - enter your windows machine's ip address in the automation skill file

## Usage

To run the Desk Companion Robot, execute the `Robot.py` file on Raspberry Pi:

```sh
python /Robot/Robot.py
```

To run windows server, execute the `main.py` file on Windows Machine:
```sh
py main.py
```
