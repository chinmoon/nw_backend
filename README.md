# Flask-AppBuilder Admin

A Flask-AppBuilder backend API project inspired by gin-quasar-admin.

## Features

- User Authentication with JWT
- CORS support
- RESTful API
- Swagger UI documentation
- MySQL database support
- Role-based access control

## Project Structure

```
nw_backend/
├── app/
│   ├── api/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── utils/
├── config/
├── migrations/
└── tests/
```

## Quick Start

1. Create virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure database in config.py

4. Run the application:
```bash
flask run
```

## API Documentation

Access Swagger UI at: http://localhost:5000/swagger/v1

## License

MIT