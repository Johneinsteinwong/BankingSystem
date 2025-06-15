# Simple Banking System

A command-line banking application that allows users to create accounts, log in, deposit, withdraw, transfer funds, and persist account data to a CSV file. Built with Python, Pydantic for data validation, and Decimal for precise arithmetic, the system is designed for simplicity and reliability, with comprehensive unit tests. This project is intended to be run using Docker.

## Features

- Create and manage bank accounts with unique IDs, names, and balances.
- Perform deposits, withdrawals, and transfers with input validation.
- Persist account data to `accounts.csv` for durability.
- Use a dictionary-based `BankingSystem` (`Dict[int, Account]`) for efficient account management.
- Validate inputs using Pydantic and handle edge cases (e.g., invalid amounts, non-existent recipients).
- Comprehensive unit tests for all functionality.

## Project Structure

```
BankingSystem/
├── data/
│   ├── accounts.csv      # CSV file for account persistence (created by program if not exists)
├── src/
│   ├── __init__.py
│   ├── main.py           # Main interactive program
│   ├── account.py        # Account class for account operations
│   ├── banking_system.py # BankingSystem class for account management
│   ├── utils.py          # Utility functions (e.g., decimal conversion)
├── tests/
│   ├── __init__.py
│   ├── test_main.py      # Tests for main.py
│   ├── test_banking_system.py # Tests for banking_system.py
│   ├── test_account.py   # Tests for account.py
│   ├── test_utils.py     # Tests for utils.py
├── Dockerfile            # Docker configuration
├── pytest.ini            # Pytest configuration for imports
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
```

## Prerequisites

- **Docker**: Required to build and run the application and tests.
- A terminal or command prompt (e.g., PowerShell on Windows, Bash on Linux/macOS).

## Clone the Repository
   ```bash
   git clone https://github.com/Johneinsteinwong/BankingSystem.git
   cd BankingSystem
   ```

## Docker Setup
### Install Docker
1. **Download and Install Docker Desktop**:
   - **Windows/macOS**: Install Docker Desktop from [Docker's official site](https://www.docker.com/products/docker-desktop/).
   - **Linux**: Follow the [Docker installation guide](https://docs.docker.com/engine/install/) for your distribution (e.g., Ubuntu, Debian).
2. **Verify Installation**:
   ```bash
   docker --version
   ```
   Ensure Docker is running (e.g., start Docker Desktop on Windows/macOS).

### Build the Docker Image
1. Navigate to the project root:
   ```bash
   cd /path/to/BankingSystem
   ```
2. Build the Docker image:
   ```bash
   docker build -t simple-banking-system .
   ```
   This creates an image named `simple-banking-system` based on `python:3.11-slim`, copying source files, tests, and dependencies to `/app`.

### Run the Main Program in Docker
Run the interactive program, mounting the `data/` folder to persist account data:
```bash
docker run -it -v "$(pwd)/data:/app/data" simple-banking-system
```
On Windows PowerShell:
```powershell
docker run -it -v "${PWD}/data:/app/data" simple-banking-system
```
On Windows Command Prompt:
```batch
docker run -it -v "%CD%\data:/app/data" simple-banking-system
```
The `-v` flag maps the `data/` folder from your project root to `/app/data` in the container. The program creates `data/accounts.csv` with headers (`id,name,balance`) if it doesn’t exist.

### Run Tests in Docker
Run pytest to execute all tests:
```bash
docker run simple-banking-system pytest tests/ -v
```
The `-v` flag provides verbose output, showing test results for `test_main.py`, `test_banking_system.py`, `test_account.py`, and `test_utils.py`.

## Example Usage
1. **Create an Account**:
   ```
   Welcome to Simple Banking System.
   Do you have an account? Type 'yes' to login, or 'no' to create an account: no
   Please enter your name to create an account: Alice
   Please enter an initial balance: 100
   Account created for Alice with ID 1 and initial balance 100.
   You can now login with your account ID.
   ```

2. **Log In and Transfer**:
   ```
   Do you have an account? Type 'yes' to login, or 'no' to create an account: yes
   Please enter your account ID to login: 1
   Welcome back, Alice! Your current balance is 100.
   Please enter 'd' to deposit, 'w' to withdraw, 't' to transfer, or 'q' to quit: t
   Enter the recipient's account ID: 2
   Recipient with ID 2 does not exist.
   ```

3. **Sample accounts.csv**:
   After creating an account for Alice:
   ```csv
   id,name,balance
   1,Alice,100
   ```

## Testing
The project includes comprehensive unit tests using pytest, covering:
- Account creation, deposit, withdrawal, and transfer operations.
- Banking system account management and CSV persistence.
- Input validation for non-numeric, negative, or invalid amounts.
- Edge cases like transfers to non-existent or same accounts.

Run tests locally or in Docker (see above). All tests are located in the `tests/` directory and use fixtures for isolated testing.

## Dependencies
Listed in `requirements.txt`:
- `pydantic`: For data validation in the `Account` class.
- `pytest`: For running unit tests.
- `python-decimal`: Built-in for precise arithmetic (no additional install needed).

## Notes
- **CSV Persistence**: The program creates `data/accounts.csv` automatically if it doesn’t exist. Ensure the `data/` folder exists on the host and is writable.
- **Volume Mounting**: The `-v` flag maps the `data/` folder to `/app/data`. Create the `data/` folder to avoid volume mount errors.
- **Absolute Imports**: The project uses absolute imports (e.g., `from banking_system import BankingSystem`), supported by `sys.path` in `main.py` and `pytest.ini` for tests.
- **Windows Paths**: Use PowerShell (`${PWD}`) or Command Prompt (`%CD%`) for volume mounts, as shown above.
- **Docker Permissions**: Ensure Docker has permission to read/write to `data/` on the host.
- **BankingSystem Configuration**: Ensure `banking_system.py` uses `csv_path='data/accounts.csv'` to write to `/app/data/accounts.csv`.