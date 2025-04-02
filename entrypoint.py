import yaml

# Load YAML config
with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

print(cfg["data"]["extensions"], cfg["db"]["name"], cfg["embedding"]["model"])


