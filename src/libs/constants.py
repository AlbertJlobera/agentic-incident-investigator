from pathlib import Path


# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

PORTFOLIO_FILE = DATA_DIR / "portfolio_executions.json"
LOGS_FILE = DATA_DIR / "execution_logs.txt"
DOCUMENTATION_DIR = DATA_DIR / "documentation"


# Investigation status
INVESTIGATING = "INVESTIGATING"
PORTFOLIO_NOT_FOUND = "PORTFOLIO_NOT_FOUND"
LOGS_NOT_FOUND = "LOGS_NOT_FOUND"
NO_INCIDENT = "NO_INCIDENT"
INCIDENT_FOUND = "INCIDENT_FOUND"