# Shopping App (Flask + Tkinter)

This is a simple shopping desktop application built with a Flask backend and a Tkinter GUI frontend. It demonstrates basic CRUD operations, API usage, and desktop GUI development using Python.

## Features

- View available items  
- Add items to a shopping cart  
- Create new items  
- View cart with quantities and total cost  

## Requirements

- Python 3.x  
- Flask  
- Requests  
- Tkinter

## Setup Instructions

### 1. (Optional) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # On macOS/Linux
venv\Scripts\activate           # On Windows
```

### 2. Install dependencies
```bash
pip install flask requests
```

## How to Run the App
### Step 1: Run the backend (Flask server)

```bash
python app.py
```

This will start the backend server at: http://127.0.0.1:5000

### Step 2: In a new terminal, run the frontend GUI
```bash
python main.py
```

This will open the desktop shopping app window.
You can view items, add them to the cart, or create new items.

## Notes
The backend uses in-memory storage, so all data resets when you restart the server.
