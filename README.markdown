# Task Manager

**Task Manager** is a modular task management web application that supports multiple storage types (memory, SQLite, JSON file). It provides the following features:

- REST API powered by FastAPI
- Command-line interface (CLI)
- Simple HTML + JavaScript frontend
- Export functionality to CSV, JSON, and Markdown formats

---

## 🚀 Quick Start (via Docker)

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/task-manager.git
   cd task-manager
   ```

2. Build and run the Docker container:
   ```bash
   docker build -t task-manager .
   docker run -p 8000:8000 task-manager
   ```

3. Access the API:
   - API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

4. Serve the frontend manually:
   ```bash
   cd frontend
   python -m http.server 8080
   ```
   Then open [http://localhost:8080](http://localhost:8080) in your browser.

## 🚀 Alternative Quick Start (via Docker Compose)

1. Clone the repository (if not already done):
   ```bash
   git clone https://github.com/your-username/task-manager.git
   cd task-manager
   ```

2. Ensure you have a `docker-compose.yml` file in the project root (create one if necessary). Run the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Access the API:
   - API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

4. Serve the frontend manually (same as above):
   ```bash
   cd frontend
   python -m http.server 8080
   ```
   Then open [http://localhost:8080](http://localhost:8080) in your browser.

---

## 🖥️ Manual Setup (Without Docker)

### Prerequisites
- Python 3.8 or higher
- `pip` package manager

### Installation
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the example environment configuration:
   ```bash
   cp config/.env.example config/.env
   ```

### Run the App
- **API (backend)**:
  ```bash
  uvicorn api:app --reload
  ```

- **CLI**:
  ```bash
  python main.py
  ```

- **Frontend**:
  ```bash
  cd frontend
  python -m http.server 8080
  ```
  Then open [http://localhost:8080](http://localhost:8080) in your browser.

---

## 🧪 Run Tests
To execute the unit tests:
```bash
python -m unittest discover -s tests
```

---

## 📁 Project Structure
```
task-manager/
├── frontend/                      # Frontend files
│   ├── index.html                 # Main HTML file
│   └── script.js                  # JavaScript logic for frontend
├── src/                           # Backend source code
│   ├── sli/                       # System-level interface
│   │   └── interface.py
│   ├── core/                      # Core utilities
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── config/
│   │       ├── .env
│   │       └── task_manager.log
│   ├── export/                    # Export functionality
│   │   ├── exporter.py
│   │   ├── csv_exporter.py
│   │   ├── json_exporter.py
│   │   └── markdown_exporter.py
│   ├── factory/                   # Storage factory
│   │   └── storage_factory.py
│   ├── iterators/                 # Task iterator
│   │   └── task_iterator.py
│   ├── models/                    # Task data model
│   │   └── task.py
│   ├── storage/                   # Storage implementations
│   │   ├── base.py
│   │   ├── jsonfile.py
│   │   ├── memory.py
│   │   └── sqlite.py
├── tests/                         # Unit tests
│   ├── sli/
│   ├── core/
│   ├── export/
│   ├── factory/
│   ├── iterators/
│   ├── models/
│   ├── storage/
│   └── test_api.py
├── api.py                         # FastAPI app
├── main.py                        # CLI entry point
├── Dockerfile                     # Docker container setup
└── README.md                      # Documentation
```

---

## 📜 License
This project is licensed under the MIT License.