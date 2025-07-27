
import csv
import json

def convert_csv_to_json(csv_file_path, json_file_path):
    """
    Convertit un fichier CSV en un fichier JSON.
    """
    data = []
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {csv_file_path} n'a pas été trouvé.")
        return

    try:
        with open(json_file_path, mode='w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"Le fichier a été converti avec succès en {json_file_path}")
    except IOError as e:
        print(f"Erreur lors de l'écriture du fichier JSON : {e}")

if __name__ == "__main__":
    CSV_FILE = 'data/RESU_BEPC_2025_74821.csv'
    JSON_FILE = 'data/results.json'
    convert_csv_to_json(CSV_FILE, JSON_FILE)
