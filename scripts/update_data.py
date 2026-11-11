from src.agents.supervisor import Supervisor
from src.config import load_config


if __name__ == "__main__":
    summary = Supervisor(load_config()).update_data()
    print(f"Fetched {len(summary.fetched)} symbol/timeframe sets.")
    if summary.failed:
        print("Some requests failed:")
        for key, reason in summary.failed.items():
            print(f"- {key}: {reason}")
