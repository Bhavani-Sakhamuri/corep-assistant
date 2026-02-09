import yaml

def load_risk_config():
    with open("config/risk_config.yaml", "r") as f:
        return yaml.safe_load(f)
