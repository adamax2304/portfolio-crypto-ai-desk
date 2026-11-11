from src.agents.supervisor import Supervisor
from src.config import load_config


if __name__ == "__main__":
    path = Supervisor(load_config()).intraday_report()
    print(f"Intraday report saved: {path}")
