import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")
CONTAINER_ENV = {
    "TENANT_ID": "",
    "CLIENT_ID": "",
    "CLIENT_SECRET": os.environ.get("CLIENT_SECRET"),
}
