# Setup Guide

Follow these steps to set up the Low2High platform on your local machine.

## Prerequisites
- Python 3.10+
- Git

## Installation

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   cd Low2High
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - **Windows (Command Prompt)**:
     ```cmd
     venv\Scripts\activate.bat
     ```
   - **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
5. **Install Playwright Browsers**:
   Since the project uses Playwright for web scraping, you must install the required browser binaries:
   ```bash
   playwright install
   ```

## Configuration

1. **Environment Variables**:
   Copy the example environment file to `.env`:
   ```bash
   cp .env.example .env
   ```
   Open the `.env` file and populate the required API keys (e.g., OpenAI API Key, Google Maps API Key).

2. **Database Setup**:
   The project uses SQLite and SQLAlchemy for database management. By default, it will create a `low2high.db` file in the project root.
   To initialize the database and create all required tables, run the following Python command from the project root (ensure your virtual environment is active):
   ```bash
   python -c "import asyncio; from src.low2high.models.database import init_db; asyncio.run(init_db())"
   ```

## Running the Application

### 1. Start the Backend API (FastAPI)
Run the FastAPI server using `uvicorn` (which is typically installed with FastAPI):
```bash
uvicorn src.low2high.main:app --reload
```
*(Adjust the import path `src.low2high.main:app` according to the actual entry point in your codebase).*

The API will be accessible at `http://localhost:8000` and Swagger UI documentation at `http://localhost:8000/docs`.

### 2. Start the Frontend Dashboard (Streamlit)
In a new terminal window (don't forget to activate the virtual environment), run:
```bash
streamlit run src/low2high/app.py
```
*(Adjust `src/low2high/app.py` according to the actual Streamlit entry point).*

The Streamlit dashboard will be accessible at `http://localhost:8501`.

## Running Tests
To run the test suite, ensure your virtual environment is activated and execute:
```bash
pytest
```
