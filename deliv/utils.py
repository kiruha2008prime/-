import os
import json
from typing import List, Dict, Type, Optional

DATA_DIR = "data"

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    for file in ["users.txt", "menu.txt", "orders.txt", "restaurants.txt", "couriers.txt"]:
        if not os.path.exists(os.path.join(DATA_DIR, file)):
            with open(os.path.join(DATA_DIR, file), "w", encoding="utf-8") as f:
                f.write("")

def read_file(filename: str) -> List[Dict]:
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [json.loads(line.strip()) for line in lines if line.strip()]

def write_file(filename: str, data: List):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        for item in data:
            # Используем to_dict(), если объект поддерживает этот метод
            if hasattr(item, 'to_dict'):
                f.write(json.dumps(item.to_dict(), ensure_ascii=False) + "\n")
            else:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

def get_next_id(filename: str) -> int:
    data = read_file(filename)
    if not data:
        return 1
    return max(item.get("id", 0) for item in data) + 1