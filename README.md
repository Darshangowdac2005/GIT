back2u-python-mysql/
├── backend/
│   ├── config/
│   │   ├── __init__.py          # Marks directory as a Python package
│   │   └── db_connector.py      # MySQL connection setup and connection utility
│   │   
│   ├── models/
│   │   ├── __init__.py          # Imports all models to simplify imports elsewhere
│   │   ├── user_model.py        # Defines the Users table structure (5-table schema)
│   │   ├── item_model.py        # Defines the Items table structure
│   │   ├── claim_model.py       # Defines the Claims table structure
│   │   ├── notification_model.py# Defines the Notifications table structure
│   │   └── category_model.py    # Defines the Categories table structure
│   │   
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py       # Handles /api/auth/login and signup
│   │   ├── item_routes.py       # Handles /api/items (reporting, public view)
│   │   └── admin_routes.py      # Handles /api/admin/claims (verification, resolution)
│   │   
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── security.py          # Handles password hashing (bcrypt) and JWT (tokens)
│   │   └── notification.py      # Handles email sending (for resolution/claim updates)
│   │   
│   ├── server.py              # Main Flask application entry point
│   ├── requirements.txt         # List of all Python dependencies (Flask, bcrypt, etc.)
│   └── .env                   # Environment variables (MySQL credentials, JWT secret)
│
├── frontend/
│   ├── assets/                  # Directory for images, logos, and fonts
│   │   └── logo.png
│   │   
│   ├── views/
│   │   ├── __init__.py
│   │   ├── login_view.py        # Flet UI for login and signup
│   │   ├── home_view.py         # Flet UI for public item listings (search, filter)
│   │   ├── report_item_view.py  # Flet UI for the lost/found reporting form
│   │   └── admin_dashboard.py   # Flet UI for admin claim verification and management
│   │   
│   ├── components/              # Reusable Flet UI elements (e.g., custom buttons, item card)
│   │   ├── navbar.py
│   │   └── item_card.py
│   │
│   ├── api_client.py            # Python module to handle requests to the Flask backend
│   ├── main.py                  # Main Flet application entry point (defines page structure)
│   └── requirements.txt         # List of all Flet dependencies (flet, requests)
│
├── .gitignore
└── README.md