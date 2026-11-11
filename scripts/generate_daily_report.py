from src.agents.supervisor import Supervisor
from src.config import load_config


if __name__ == "__main__":
    path = Supervisor(load_config()).daily_report()
    print(f"Daily report saved: {path}")
