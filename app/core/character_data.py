import json
from pathlib import Path


CHARACTER_DATA_FOLDER = Path(__file__).resolve().parents[2] / "data" / "characters"


def load_character(filename):
	file_path = CHARACTER_DATA_FOLDER / filename

	with open(file_path, "r", encoding="utf-8") as file:
		return json.load(file)
