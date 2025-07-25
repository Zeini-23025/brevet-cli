import csv
import os
from collections import Counter
import sys

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data(filename="data/RESU_BEPC_2025_74821.csv"):
    """
    Loads student data from a CSV file into a list of dictionaries.
    Handles potential file not found errors.
    """
    data = []
    try:
        with open(filename, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                try:
                    row['Num_Bepc'] = int(row['Num_Bepc'])
                    row['Moyenne_Bepc'] = float(row['Moyenne_Bepc'])
                    data.append(row)
                except (ValueError, KeyError) as e:
                    print(f"Avertissement: Ligne ignorée pour cause de données invalides: {row}. Erreur: {e}")
    except FileNotFoundError:
        print(f"Erreur: Le fichier '{filename}' est introuvable.")
        return None
    except Exception as e:
        print(f"Une erreur inattendue est survenue: {e}")
        return None
    return data

def advanced_search(data, num_bepc):
    """
    Searches for a student by Num_Bepc and returns all their information.
    """
    for student in data:
        if student['Num_Bepc'] == num_bepc:
            return student
    return None

def simple_search(data, num_bepc):
    """
    Searches for a student by Num_Bepc and returns their name, average, and decision.
    """
    student = advanced_search(data, num_bepc)
    if student:
        return {
            'NOM': student.get('NOM', 'N/A'),
            'Moyenne_Bepc': student.get('Moyenne_Bepc', 'N/A'),
            'Decision': student.get('Decision', 'N/A')
        }
    return None

def calculate_general_stats(data):
    """
    Calculates and returns general statistics for all students.
    """
    if not data:
        return "Aucune donnée à analyser."

    total_students = len(data)
    decisions = [s['Decision'] for s in data if 'Decision' in s]
    decision_counts = Counter(decisions)
    
    admis_count = decision_counts.get('Admis', 0)
    
    pass_rate = (admis_count / total_students) * 100 if total_students > 0 else 0
    
    averages = [s['Moyenne_Bepc'] for s in data if 'Moyenne_Bepc' in s]
    overall_average = sum(averages) / len(averages) if averages else 0

    stats = (
        f"Statistiques Générales :\n"
        f"------------------------\n"
        f"Nombre total d'étudiants : {total_students}\n"
        f"Nombre d'admis : {admis_count}\n"
        f"Taux de réussite : {pass_rate:.2f}%\n"
        f"Moyenne générale de tous les étudiants : {overall_average:.2f}\n"
    )
    return stats

def get_grouped_data(data, group_key):
    """Helper function to get grouped data."""
    grouped_data = {}
    for student in data:
        key = student.get(group_key)
        if key:
            if key not in grouped_data:
                grouped_data[key] = {'total': 0, 'admis': 0, 'averages': []}
            grouped_data[key]['total'] += 1
            if student.get('Decision') == 'Admis':
                grouped_data[key]['admis'] += 1
            if 'Moyenne_Bepc' in student:
                grouped_data[key]['averages'].append(student['Moyenne_Bepc'])
    return grouped_data

def calculate_grouped_stats(data, group_key):
    """
    Calculates and returns statistics grouped by a specific key (e.g., 'WILAYA').
    """
    if not data:
        return "Aucune donnée à analyser."

    grouped_data = get_grouped_data(data, group_key)
    
    report = f"Statistiques par {group_key} :\n"
    report += "------------------------------------\n"
    
    sorted_groups = sorted(grouped_data.items(), key=lambda item: item[1]['total'], reverse=True)

    for key, values in sorted_groups:
        total = values['total']
        admis = values['admis']
        pass_rate = (admis / total) * 100 if total > 0 else 0
        avg_score = sum(values['averages']) / len(values['averages']) if values['averages'] else 0
        report += (
            f"\n{group_key}: {key}\n"
            f"  Nombre d'étudiants : {total}\n"
            f"  Nombre d'admis : {admis}\n"
            f"  Taux de réussite : {pass_rate:.2f}%\n"
            f"  Moyenne : {avg_score:.2f}\n"
        )
    return report

def plot_decision_distribution(data):
    """Plots the distribution of decisions (Admis vs. others)."""
    decisions = [s['Decision'] for s in data if 'Decision' in s]
    decision_counts = Counter(decisions)
    
    plt.figure(figsize=(8, 6))
    plt.pie(decision_counts.values(), labels=decision_counts.keys(), autopct='%1.1f%%', startangle=140)
    plt.title('Répartition des décisions')
    plt.ylabel('')
    plt.savefig('decision_distribution.png')
    print("Graphique 'decision_distribution.png' sauvegardé.")

def plot_pass_rate_by_group(data, group_key, top_n=15):
    """Plots the pass rate for the top N groups."""
    grouped_data = get_grouped_data(data, group_key)
    
    sorted_groups = sorted(grouped_data.items(), key=lambda item: item[1]['total'], reverse=True)[:top_n]
    
    labels = [g[0] for g in sorted_groups]
    pass_rates = [(g[1]['admis'] / g[1]['total']) * 100 if g[1]['total'] > 0 else 0 for g in sorted_groups]
    
    plt.figure(figsize=(12, 8))
    plt.barh(labels, pass_rates, color='skyblue')
    plt.xlabel('Taux de réussite (%)')
    plt.title(f'Taux de réussite par {group_key} (Top {top_n})')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(f'pass_rate_by_{group_key}.png')
    print(f"Graphique 'pass_rate_by_{group_key}.png' sauvegardé.")

def main():
    """
    Main function to run the student analysis script.
    """
    student_data = load_data()
    if student_data is None:
        return

    while True:
        clear_screen()
        print("\n--- Menu Principal ---")
        print("1. Recherche avancée d'un étudiant")
        print("2. Recherche simple d'un étudiant")
        print("3. Afficher les statistiques générales")
        print("4. Afficher les statistiques par WILAYA")
        print("5. Afficher les statistiques par LIEU_NAIS")
        print("6. Générer des graphiques")
        print("7. Quitter")
        
        choice = input("Veuillez choisir une option (1-7) : ")

        if choice == '1':
            try:
                num_bepc = int(input("Entrez le Num_Bepc de l'étudiant : "))
                result = advanced_search(student_data, num_bepc)
                clear_screen()
                print("\n--- Résultat de la recherche avancée ---")
                if result:
                    for key, value in result.items():
                        print(f"{key}: {value}")
                else:
                    print("Aucun étudiant trouvé avec ce Num_Bepc.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer un numéro.")
            input("\nAppuyez sur Entrée pour continuer...")

        elif choice == '2':
            try:
                num_bepc = int(input("Entrez le Num_Bepc de l'étudiant : "))
                result = simple_search(student_data, num_bepc)
                clear_screen()
                print("\n--- Résultat de la recherche simple ---")
                if result:
                    print(f"NOM: {result['NOM']}\nMoyenne_Bepc: {result['Moyenne_Bepc']}\nDecision: {result['Decision']}")
                else:
                    print("Aucun étudiant trouvé avec ce Num_Bepc.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer un numéro.")
            input("\nAppuyez sur Entrée pour continuer...")

        elif choice == '3':
            clear_screen()
            stats = calculate_general_stats(student_data)
            print(stats)
            input("\nAppuyez sur Entrée pour continuer...")

        elif choice == '4':
            clear_screen()
            stats = calculate_grouped_stats(student_data, 'WILAYA')
            print(stats)
            input("\nAppuyez sur Entrée pour continuer...")
            
        elif choice == '5':
            clear_screen()
            print("Note: La liste des lieux de naissance peut être très longue.")
            limit_str = input("Combien de lieux afficher (laissez vide pour tous) ? ")
            try:
                limit = int(limit_str) if limit_str else None
            except ValueError:
                limit = None

            stats = calculate_grouped_stats(student_data, 'LIEU_NAIS')
            
            if limit:
                lines = stats.split('\n')
                header = lines[:2]
                groups = '\n'.join(lines[2:]).split('\n\n')
                
                print('\n'.join(header))
                for group in groups[:limit]:
                    print('\n' + group)
            else:
                print(stats)

            input("\nAppuyez sur Entrée pour continuer...")

        elif choice == '6':
            if not MATPLOTLIB_AVAILABLE:
                print("La bibliothèque Matplotlib n'est pas installée.")
                install = input("Voulez-vous l'installer maintenant (pip install matplotlib) ? (o/n): ")
                if install.lower() == 'o':
                    os.system(f"{sys.executable} -m pip install matplotlib")
                    print("\nMatplotlib a été installé. Veuillez relancer le script.")
                else:
                    print("Opération annulée.")
                input("\nAppuyez sur Entrée pour continuer...")
                continue

            clear_screen()
            print("\n--- Génération de Graphiques ---")
            print("1. Répartition des décisions (Admis/Non Admis)")
            print("2. Taux de réussite par WILAYA")
            print("3. Taux de réussite par LIEU_NAIS (Top 15)")
            
            plot_choice = input("Choisissez un graphique à générer (1-3) : ")
            
            if plot_choice == '1':
                plot_decision_distribution(student_data)
            elif plot_choice == '2':
                plot_pass_rate_by_group(student_data, 'WILAYA')
            elif plot_choice == '3':
                plot_pass_rate_by_group(student_data, 'LIEU_NAIS')
            else:
                print("Choix invalide.")
            
            input("\nAppuyez sur Entrée pour continuer...")

        elif choice == '7':
            print("Merci d'avoir utilisé le script. Au revoir !")
            break
        else:
            print("Choix invalide, veuillez réessayer.")
            input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()