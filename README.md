# herkey-demo

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

Welcome to the herkey-demo project! This project is designed to...

## Installation

To install the project, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/herkey-demo.git
   ```
2. Navigate to the project directory:
   ```sh
   cd herkey-demo
   ```
3. Create a virtual environment for local setup:
   ```sh
   python3 -m venv env
   ```
4. Activate the virtual environment:
   ```sh
   source env/bin/activate
   ```
5. Install the dependencies:
   ```sh
   pip install -r /herkey/requirements.txt
   ```

## Usage

To use the project, follow these steps:

Change the directory to /herkey

1. Apply the migrations:
   ```sh
   python manage.py migrate
   ```
2. Start the development server:
   ```sh
    python manage.py runserver
   ```
   This will start the application and you can access it at `http://localhost:8000`.
