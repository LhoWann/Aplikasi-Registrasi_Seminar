import csv
from datetime import datetime
from tkinter import messagebox
from config import DATA_FILE

def save_data_to_csv(participants_list: list[dict], file_path=DATA_FILE):
    try:
        fieldnames = participants_list[0].keys() if participants_list \
                     else ['nama', 'email', 'institusi', 'waktu_daftar']
        
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for participant in participants_list:
                participant_to_save = participant.copy()
                if 'waktu_daftar' in participant_to_save and \
                   isinstance(participant_to_save['waktu_daftar'], datetime):
                    participant_to_save['waktu_daftar'] = participant_to_save['waktu_daftar'].isoformat()
                writer.writerow(participant_to_save)
    except Exception as e:
        messagebox.showerror("Error Menyimpan Data", f"Gagal menyimpan data ke file: {e}")

def load_data_from_csv(file_path=DATA_FILE) -> list[dict]:
    participants = []
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'waktu_daftar' in row and row['waktu_daftar']:
                    try:
                        row['waktu_daftar'] = datetime.fromisoformat(row['waktu_daftar'])
                    except ValueError:
                        pass 
                participants.append(row)
    except FileNotFoundError:
        pass
    except Exception as e:
        messagebox.showerror("Error Memuat Data", f"Gagal memuat data dari file: {e}")
    return participants