import re
from datetime import datetime
from data_handling import load_data_from_csv, save_data_to_csv
from config import MAX_PARTICIPANTS 

class Seminar_Registration:
    def __init__(self):
        self.participants = load_data_from_csv()

    def _is_valid_string_input(self, input_str: str, nama_field: str) -> tuple[bool, str, str]:
        string_diproses = input_str.strip()
        if not string_diproses:
            return False, f"{nama_field} tidak boleh kosong.", ""

        if nama_field in ("Nama", "Institusi"):
            pattern = r"^(?=.*[a-zA-ZÀ-ÿ])[a-zA-ZÀ-ÿ\s'-]+$"
            if not re.fullmatch(pattern, string_diproses):
                return False, f"{nama_field} hanya boleh berisi huruf, spasi, apostrof ('), dan tanda hubung (-). Pastikan ada setidaknya satu huruf.", ""
            
            if all(char in " '-" for char in string_diproses):
                 return False, f"{nama_field} tidak boleh hanya terdiri dari spasi atau karakter khusus.", ""

        return True, "Input valid.", string_diproses

    def validate_email(self, email: str) -> bool:
        if not email: return False
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))

    def register_participant(self, nama: str, email: str, institusi: str) -> tuple[bool, str]:
        if len(self.participants) >= MAX_PARTICIPANTS:
            return False, f"Pendaftaran Gagal. Kapasitas seminar sudah penuh ({MAX_PARTICIPANTS} peserta)."

        is_valid_nama, msg_nama, proc_nama = self._is_valid_string_input(nama, "Nama")
        if not is_valid_nama: return False, msg_nama

        if not email: return False, "Email tidak boleh kosong."
        if not self.validate_email(email): return False, "Format email tidak valid."

        is_valid_inst, msg_inst, proc_institusi = self._is_valid_string_input(institusi, "Institusi")
        if not is_valid_inst: return False, msg_inst
        
        if any(p['email'].lower() == email.lower() for p in self.participants):
            return False, "Email sudah terdaftar."

        participant = {
            'nama': proc_nama, 'email': email, 'institusi': proc_institusi,
            'waktu_daftar': datetime.now()
        }
        self.participants.append(participant)
        save_data_to_csv(self.participants)
        return True, "Registrasi berhasil."

    def sequential_search(self, keyword: str) -> list[dict]:
        if not keyword: return list(self.participants) 
        keyword_l = keyword.lower()
        return [p for p in self.participants if 
                keyword_l in p['nama'].lower() or \
                keyword_l in p['email'].lower() or \
                keyword_l in p['institusi'].lower()]

    def _merge(self, left: list[dict], right: list[dict], key: str) -> list[dict]:
        result, l_idx, r_idx = [], 0, 0
        while l_idx < len(left) and r_idx < len(right):
            l_val, r_val = left[l_idx].get(key), right[r_idx].get(key)
            if isinstance(l_val, str) and isinstance(r_val, str): cmp_l, cmp_r = l_val.lower(), r_val.lower()
            elif isinstance(l_val, datetime) and isinstance(r_val, datetime): cmp_l, cmp_r = l_val, r_val
            else: cmp_l, cmp_r = str(l_val).lower(), str(r_val).lower()
            
            if cmp_l <= cmp_r: result.append(left[l_idx]); l_idx += 1
            else: result.append(right[r_idx]); r_idx += 1
        result.extend(left[l_idx:]); result.extend(right[r_idx:])
        return result

    def merge_sort(self, data: list[dict], key: str) -> list[dict]:
        if len(data) <= 1: return data
        mid = len(data) // 2
        left_half = self.merge_sort(data[:mid], key)
        right_half = self.merge_sort(data[mid:], key)
        return self._merge(left_half, right_half, key)

    def sort_participants(self, key: str = 'waktu_daftar', reverse: bool = False) -> list[dict]:
        data_to_sort = list(self.participants) 
        sorted_data = self.merge_sort(data_to_sort, key)
        return sorted_data[::-1] if reverse else sorted_data

    def delete_participant(self, email: str) -> tuple[bool, str]:
        initial_count = len(self.participants)
        self.participants = [p for p in self.participants if p['email'].lower() != email.lower()]
        if len(self.participants) < initial_count:
            save_data_to_csv(self.participants)
            return True, "Peserta berhasil dihapus."
        return False, "Peserta dengan email tersebut tidak ditemukan."
