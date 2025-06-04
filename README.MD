# Aplikasi Registrasi Seminar

## A. Tujuan Program

**Tujuan utama** dari program Sistem Pendaftaran Seminar ini adalah untuk menyediakan sebuah aplikasi desktop yang  **memudahkan pengelolaan data peserta seminar**. Ini mencakup proses pendaftaran peserta baru, menampilkan daftar peserta, mencari peserta tertentu, mengurutkan daftar peserta berdasarkan kriteria tertentu, dan menghapus data peserta jika diperlukan. Program ini dirancang untuk menyimpan data secara persisten dalam sebuah file CSV.

## B. Fitur Program

Program ini memiliki beberapa fitur utama:

### 1. Pendaftaran Peserta Baru

    a. Pengguna dapat memasukkan**nama lengkap, alamat email, dan asal institusi** peserta melalui form input.

    b. Sistem melakukan**validasi input** , termasuk format email dan keunikan email (tidak boleh ada email yang sama terdaftar.

    c. Data peserta yang berhasil didaftarkan akan disimpan beserta**waktu pendaftaran otomatis** .

### 2. Menampilkan Daftar Peserta

    a. Seluruh peserta yang terdaftar ditampilkan dalam sebuah**tabel interaktif** .

    b. Informasi yang ditampilkan meliputi nama, email, institusi, dan waktu pendaftaran.

### 3. Pencarian Peserta

    a. Pengguna dapat**mencari peserta** berdasarkan kata kunci.

    b. Pencarian dilakukan pada field nama, email, dan institusi.

### 4. Pengurutan Peserta

    a. Daftar peserta dapat**diurutkan** berdasarkan "Waktu Daftar" atau "Nama Peserta".

    b. Pengurutan dapat dilakukan secara**Ascending (menaik)** atau  **Descending (menurun)**.

### 5. Penghapusan Peserta

    a. Pengguna dapat**memilih peserta dari tabel** dan menghapusnya.

    b. Ada**konfirmasi** sebelum data peserta benar-benar dihapus.

    c. Penghapusan dilakukan berdasarkan alamat email peserta.

### 6. Penyimpanan Data

    a. Semua data peserta**disimpan dalam sebuah file CSV** (`dummy_peserta.csv`).

    b. Data akan**dimuat saat aplikasi dimulai** dan **disimpan setiap kali ada perubahan** (pendaftaran atau penghapusan).

### 7. Antarmuka Pengguna Grafis (GUI)

    a. Aplikasi memiliki**antarmuka yang ramah pengguna** yang dibangun menggunakan Tkinter.

    b. Tata letak dan gaya widget diatur untuk kemudahan penggunaan.

## C. Algoritma yang Digunakan

### 1. Algoritma Pencarian (Searching) --> Sequential Search

- **Cara Kerja** : Algoritma ini bekerja dengan cara memeriksa setiap item dalam kumpulan data (dalam hal ini, daftar peserta) satu per satu, dari awal hingga akhir, sampai item yang dicari ditemukan atau seluruh kumpulan data telah diperiksa.
- **Implementasi** : Pada file `seminar_backend.py`, metode `sequential_search(self, keyword: str)` melakukan pencarian ini. Jika `keyword` diberikan, metode akan mengiterasi list `self.participants`. Untuk setiap peserta, ia akan memeriksa apakah `keyword` (dalam huruf kecil) terkandung dalam nama, email, atau institusi peserta (juga dalam huruf kecil). Jika `keyword` kosong, metode akan mengembalikan seluruh daftar peserta.

### 2. Algoritma Pengurutan (Sorting) --> Merge Sort

1. Cara Kerja:

* **Divide (Pilah)** : Daftar data yang belum terurut dibagi menjadi dua sub-daftar (kiri dan kanan) secara rekursif hingga setiap sub-daftar hanya berisi satu elemen (yang secara definisi sudah terurut).
* **Conquer (Taklukkan/Gabung)** : Sub-daftar yang sudah terurut kemudian digabungkan kembali (di- *merge* ) secara berurutan untuk menghasilkan daftar yang sepenuhnya terurut. Proses penggabungan membandingkan elemen dari kedua sub-daftar dan menempatkannya dalam urutan yang benar di daftar hasil.

2. Implementasi:

* Di file `seminar_backend.py`, metode `sort_participants` memanggil `merge_sort`.
* Metode `merge_sort(self, data: list[dict], key: str)` mengimplementasikan logika rekursif pembagian daftar.
* Metode `_merge(self, left: list[dict], right: list[dict], key: str)` bertugas menggabungkan dua sub-daftar (`left` dan `right`) yang sudah terurut berdasarkan `key` yang diberikan (misalnya 'nama' atau 'waktu_daftar'). Metode ini menangani perbandingan untuk tipe data string (secara case-insensitive) dan datetime.
* Pengurutan bisa dilakukan secara menaik (Ascending) atau menurun (Descending) berdasarkan parameter `reverse`.

## D. `config.py`

### **1. Tujuan**

File ini berfungsi sebagai tempat untuk menyimpan konfigurasi global atau konstanta yang digunakan di berbagai bagian aplikasi. Ini memudahkan pengelolaan dan perubahan nilai-nilai konfigurasi tanpa harus mengubah kode di banyak tempat.

### 2. Variabel Global

* **`DATA_FILE = 'dummy_peserta.csv'`** :
  * Menentukan nama file CSV yang digunakan untuk menyimpan dan memuat data peserta seminar.
* **`APP_SIZE = (950, 700)`** :
  * Sebuah tuple yang menentukan ukuran default window aplikasi dalam piksel (lebar, tinggi). Lebarnya adalah 950 piksel dan tingginya 700 piksel.

## E. `data_handling.py`

### 1. Tujuan

File ini bertanggung jawab untuk menangani operasi input/output (I/O) data, khususnya untuk membaca dan menulis data peserta seminar ke dan dari file CSV. Ini memisahkan logika penanganan file dari logika bisnis utama dan antarmuka pengguna.

### 2. Fungsi

#### `save_data_to_csv(participants_list: list[dict], file_path=DATA_FILE)`:

- Menyimpan daftar peserta (`participants_list`) ke file CSV.
- `participants_list`: Sebuah list yang berisi dictionary, di mana setiap dictionary merepresentasikan satu peserta.
- `file_path`: Path ke file CSV tujuan. Menggunakan `DATA_FILE` dari `config.py` sebagai default.
- Menentukan `fieldnames` (nama kolom) berdasarkan kunci dari dictionary pertama dalam list, atau menggunakan field default jika list kosong.
- Membuka file dalam mode tulis (`'w'`).
- Menggunakan `csv.DictWriter` untuk menulis data.
- Menulis header (nama kolom) terlebih dahulu.
- Melakukan iterasi melalui `participants_list`:
  - Membuat salinan dari dictionary peserta untuk menghindari modifikasi objek asli.
  - Jika ada field `'waktu_daftar'` dan nilainya adalah objek `datetime`, maka akan diubah menjadi format string ISO (misalnya, `'2023-10-27T14:30:00'`) sebelum disimpan.
  - Menulis baris data peserta ke file CSV.
- Menangani potensi `Exception` saat menyimpan data dan menampilkan pesan error menggunakan `messagebox.showerror`.

#### `load_data_from_csv(file_path=DATA_FILE) -> list[dict]`:

* Memuat data peserta dari file CSV.
* `file_path`: Path ke file CSV sumber. Menggunakan `DATA_FILE` dari `config.py` sebagai default.
* Menginisialisasi list kosong `participants`.
* Membuka file dalam mode baca (`'r'`).
* Menggunakan `csv.DictReader` untuk membaca data sebagai dictionary per baris.
* Melakukan iterasi melalui setiap baris (`row`) dalam file CSV:
  * Jika ada field `'waktu_daftar'` dan nilainya tidak kosong:
    * Mencoba mengubah string waktu pendaftaran (yang diharapkan dalam format ISO) kembali menjadi objek `datetime` menggunakan `datetime.fromisoformat()`.
    * Jika terjadi `ValueError` saat konversi (misalnya, format tidak sesuai), nilai tersebut akan dilewati (tidak diubah) dan tetap sebagai string.
  * Menambahkan dictionary `row` (yang merepresentasikan satu peserta) ke list `participants`.
* Menangani `FileNotFoundError` jika file tidak ditemukan (dalam kasus ini, fungsi akan mengembalikan list kosong, memungkinkan aplikasi membuat file baru saat data pertama disimpan).
* Menangani potensi `Exception` lain saat memuat data dan menampilkan pesan error menggunakan `messagebox.showerror`.
* Mengembalikan list `participants` yang berisi data peserta yang telah dimuat.

## F. `seminar_backend.py`

### **1. Tujuan**

File ini berisi logika bisnis (backend) untuk aplikasi pendaftaran seminar. Kelas `Seminar_Registration` menangani semua operasi data terkait peserta, seperti validasi input, registrasi, pencarian, pengurutan, dan penghapusan peserta. File ini juga berinteraksi dengan `data_handling.py` untuk memuat dan menyimpan data peserta ke/dari file CSV.

### 2. `class Seminar_Registration.py`

`__init__(self)`:

* Konstruktor kelas.
* Menginisialisasi `self.participants` dengan memuat data peserta dari file CSV menggunakan `load_data_from_csv()`.

### `3. _is_valid_string_input(self, input_str: str, nama_field: str) -> tuple[bool, str, str]`:

* Metode privat untuk memvalidasi input string (untuk nama dan institusi).
* `input_str`: String yang akan divalidasi.
* `nama_field`: Nama field yang divalidasi (misalnya, "Nama", "Institusi") untuk pesan error yang lebih deskriptif.
* Memeriksa apakah string kosong setelah di-`strip()`.
* Untuk field "Nama" dan "Institusi":

  * Menggunakan ekspresi reguler (`pattern = r"^(?=.*[a-zA-ZÀ-ÿ])[a-zA-ZÀ-ÿ\s'-]+$"`) untuk memastikan input hanya berisi huruf, spasi, apostrof ('), dan tanda hubung (-), dan harus mengandung setidaknya satu huruf.
  * Memeriksa apakah input hanya terdiri dari spasi atau karakter khusus.
* Mengembalikan tuple: `(status_validasi: bool, pesan_error/sukses: str, string_diproses: str)`.

### 4. `validate_email(self, email: str) -> bool`:

* Memvalidasi format alamat email menggunakan ekspresi reguler (`pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'`).
* Memeriksa apakah email kosong.
* Mengembalikan `True` jika email valid, `False` jika tidak.

### 5. `register_participant(self, nama: str, email: str, institusi: str) -> tuple[bool, str]`:

* Melakukan registrasi peserta baru.
* Memvalidasi input `nama` menggunakan `_is_valid_string_input()`.
* Memvalidasi input `email` (tidak kosong dan format valid menggunakan `validate_email()`).
* Memvalidasi input `institusi` menggunakan `_is_valid_string_input()`.
* Memeriksa apakah email sudah terdaftar (case-insensitive).
* Jika semua validasi berhasil dan email belum terdaftar:

  * Membuat dictionary `participant` yang berisi nama, email, institusi, dan waktu pendaftaran (`datetime.now()`).
  * Menambahkan peserta baru ke list `self.participants`.
  * Menyimpan data peserta yang sudah diperbarui ke file CSV menggunakan `save_data_to_csv()`.
  * Mengembalikan `(True, "Registrasi berhasil.")`.
* Jika ada kegagalan validasi atau email sudah terdaftar, mengembalikan `(False, pesan_error_yang_sesuai).`

### 6.`sequential_search(self, keyword: str) -> list[dict]`:

* Melakukan pencarian sekuensial (linear search) pada daftar peserta.
* Jika `keyword` kosong, mengembalikan seluruh daftar peserta.
* Mengubah `keyword` menjadi huruf kecil untuk pencarian case-insensitive.
* Mencari `keyword` dalam field 'nama', 'email', dan 'institusi' (semuanya diubah ke huruf kecil) dari setiap peserta.
* Mengembalikan list berisi dictionary peserta yang cocok dengan kriteria pencarian.

### 7.`_merge(self, left: list[dict], right: list[dict], key: str) -> list[dict]`:

* Metode privat, bagian dari algoritma Merge Sort.
* Menggabungkan dua sub-list (`left` dan `right`) yang sudah terurut berdasarkan `key` tertentu.
* Menangani perbandingan untuk string (case-insensitive) dan objek `datetime`.
* Mengembalikan list hasil penggabungan yang terurut.

### 8.`merge_sort(self, data: list[dict], key: str) -> list[dict]`:

* Metode privat yang mengimplementasikan algoritma Merge Sort secara rekursif.
* `data`: List dictionary peserta yang akan diurutkan.
* `key`: Kunci dalam dictionary yang digunakan sebagai dasar pengurutan (misalnya, 'nama', 'waktu_daftar').
* Membagi list menjadi dua bagian, mengurutkan masing-masing bagian secara rekursif, lalu menggabungkannya menggunakan `_merge()`.
* Mengembalikan list data yang sudah terurut.

### 9.`sort_participants(self, key: str = 'waktu_daftar', reverse: bool = False) -> list[dict]`:

* Mengurutkan daftar peserta.
* `key`: Kunci untuk pengurutan (default 'waktu_daftar').
* `reverse`: `True` untuk urutan menurun (descending), `False` untuk urutan menaik (ascending, default).
* Membuat salinan dari `self.participants` agar data asli tidak termodifikasi secara langsung oleh proses pengurutan.
* Menggunakan `merge_sort()` untuk mengurutkan data.
* Jika `reverse` adalah `True`, membalik urutan list yang sudah diurutkan.
* Mengembalikan list peserta yang sudah diurutkan.

### 10.`delete_participant(self, email: str) -> tuple[bool, str]`:

* Menghapus peserta berdasarkan alamat email.
* Membuat list baru yang berisi peserta yang email-nya (case-insensitive) tidak cocok dengan `email` yang diberikan.
* Jika jumlah peserta berkurang (artinya ada yang dihapus):

  * Memperbarui `self.participants` dengan list baru.
  * Menyimpan perubahan ke file CSV menggunakan `save_data_to_csv()`.
  * Mengembalikan `(True, "Peserta berhasil dihapus.")`.
* Jika tidak ada peserta yang dihapus (email tidak ditemukan), mengembalikan `(False, "Peserta dengan email tersebut tidak ditemukan.")`.

# G. `gui_app.py`

## 1. Tujuan:

File ini mendefinisikan antarmuka pengguna grafis (GUI) untuk aplikasi Sistem Pendaftaran Seminar menggunakan pustaka Tkinter. `class` `ParticipantApp` bertanggung jawab untuk membuat semua widget (seperti label, input field, tombol, tabel), mengatur tata letaknya, dan menghubungkan aksi pengguna (misalnya, klik tombol) dengan fungsi-fungsi yang sesuai di backend (`Seminar_Registration`).

## 2. Fungsi

### `class` `ParticipantApp :`

#### **`__init__(self, root)`:**

* Konstruktor kelas.
* `root`: Argumen yang merupakan instance dari `tk.Tk()`, yaitu window utama aplikasi.
* Mengatur judul window menjadi "Sistem Pendaftaran Seminar".
* Menginisialisasi `Seminar_Registration` untuk mengakses logika bisnis.
* Memanggil `_setup_styles()` untuk mengkonfigurasi gaya widget ttk.
* Memanggil `_create_widgets()` untuk membuat semua elemen GUI.
* Memanggil `refresh_table()` untuk memuat dan menampilkan data awal pada tabel.
* Memberikan fokus awal ke field input nama jika ada.

#### **`_setup_styles(self)`:**

* Metode privat untuk mengkonfigurasi gaya visual dari widget `ttk`.
* Menggunakan tema "clam".
* Mengatur font untuk `Treeview.Heading` dan padding serta font untuk `TButton`, `TLabel`, `TEntry`, dan `TCombobox`.

#### **`_create_widgets(self)`:**

* Metode privat yang bertanggung jawab untuk membuat dan menata semua widget GUI.
* **Frame Input (`f_input`):**
  * Berisi label dan entry untuk "Nama Lengkap:", "Alamat Email:", dan "Asal Institusi:".
  * Setiap entry disimpan sebagai atribut instance (misalnya, `self.entry_nama`).
  * Tombol "Daftarkan Peserta" yang memanggil `self.on_register` saat diklik.
* **Frame Kontrol (`f_ctrl`):**
  * Berisi field input "Cari Peserta:", tombol "Cari" (memanggil `self.on_search`), dan binding event `<Return>` pada field pencarian ke `self.on_search`.
  * Dropdown (Combobox) "Urutkan:" dengan opsi "Waktu Daftar" dan "Nama".
  * Dropdown (Combobox) untuk urutan ("Ascending", "Descending").
  * Tombol "Urutkan" yang memanggil `self.on_sort`.
  * Tombol "Hapus" yang memanggil `self.on_delete`.
* **Frame Tabel Data (`f_tbl`):**
  * Berisi `ttk.Treeview` (`self.tabel`) untuk menampilkan daftar peserta.
  * Mendefinisikan kolom-kolom tabel: "Nama Peserta", "Alamat Email", "Asal Institusi", "Waktu Pendaftaran".
  * Mengatur lebar, penjangkaran (anchor), dan kemampuan peregangan (stretch) untuk setiap kolom.
  * Menambahkan *scrollbar* vertikal dan horizontal ke tabel.

#### **`_format_datetime(self, dt_obj)`:**

* Metode privat untuk memformat objek `datetime` menjadi string dengan format 'YYYY-MM-DD HH:MM:SS'.
* Jika input bukan objek `datetime`, akan dikembalikan sebagai string.

#### **`refresh_table(self, data_list=None)`:**

* Menghapus semua item yang ada di tabel.
* Mengisi tabel dengan data peserta.
* Jika `data_list` disediakan (misalnya, hasil pencarian), data tersebut yang akan ditampilkan.
* Jika tidak, data diambil dari `self.seminar_system.sort_participants()` berdasarkan kriteria pengurutan yang dipilih pada GUI.
* Setiap baris data peserta dimasukkan ke dalam tabel.

#### **`on_register(self)`:**

* Dipanggil saat tombol "Daftarkan Peserta" diklik.
* Mengambil nilai dari field input nama, email, dan institusi.
* Melakukan validasi dasar untuk memastikan semua field terisi. Jika tidak, menampilkan pesan peringatan.
* Memanggil `self.seminar_system.register_participant()` untuk memproses pendaftaran.
* Menampilkan pesan informasi (berhasil atau gagal) dari hasil registrasi.
* Jika registrasi berhasil, mengosongkan field input dan memanggil `self.refresh_table()` untuk memperbarui tampilan tabel.

#### **`on_search(self, event=None)`:**

* Dipanggil saat tombol "Cari" diklik atau tombol Enter ditekan di field pencarian.
* Mengambil kata kunci pencarian dari `self.entry_search`.
* Memanggil `self.seminar_system.sequential_search()` untuk mencari peserta berdasarkan kata kunci.
* Jika tidak ada hasil dan kata kunci tidak kosong, tampilkan pesan informasi.
* Memanggil `self.refresh_table()` dengan hasil pencarian (`res`) sebagai `data_list`.

#### **`on_sort(self)`:**

* Dipanggil saat tombol "Urutkan" diklik.
* Memanggil `self.refresh_table()`. Metode ini secara otomatis akan menggunakan opsi pengurutan yang dipilih dari `combo_sort_by` dan `combo_sort_order`.

#### **`on_delete(self)`:**

* Dipanggil saat tombol "Hapus" diklik.
* Mendapatkan item (baris) yang sedang dipilih di tabel (`self.tabel.focus()`).
* Jika tidak ada item yang dipilih, tampilkan pesan peringatan.
* Mengambil nilai email (identifikator unik) dan nama dari item yang dipilih.
* Menampilkan dialog konfirmasi penghapusan.
* Jika pengguna mengkonfirmasi, memanggil `self.seminar_system.delete_participant()` dengan email peserta yang akan dihapus.
* Menampilkan pesan informasi mengenai hasil operasi penghapusan.
* Memanggil `self.refresh_table()` untuk memperbarui tampilan tabel.

# H. `main.py`

# **1. Tujuan :**

File ini berfungsi sebagai titik masuk utama (entry point) untuk menjalankan aplikasi desktop Sistem Pendaftaran Seminar. Tugas utamanya adalah menginisialisasi window utama Tkinter, membuat instance dari kelas `ParticipantApp` (yang mendefinisikan GUI), mengatur ukuran dan posisi window aplikasi di tengah layar, dan memulai *event loop* Tkinter.

## 2. Struktur :

* ### **Import Modul:**

  * `tkinter` sebagai `tk`: Digunakan untuk membuat elemen-elemen dasar GUI.
  * `ParticipantApp` dari `gui_app`: Kelas yang berisi logika dan tata letak antarmuka pengguna aplikasi.
  * `APP_SIZE` dari `config`: Konstanta yang menentukan ukuran window aplikasi (lebar, tinggi).
* ### **Blok `if __name__ == "__main__":` :**

  * `root = tk.Tk()`: Membuat instance window utama Tkinter.
  * `app_gui = ParticipantApp(root)`: Membuat instance dari kelas `ParticipantApp`, yang akan membangun seluruh antarmuka pengguna di dalam `root`.
  * **Pengaturan Geometri Window:**
    * `window_width = APP_SIZE[0]`: Mengambil lebar window dari konfigurasi.
    * `window_height = APP_SIZE[1]`: Mengambil tinggi window dari konfigurasi.
    * `screen_width = root.winfo_screenwidth()`: Mendapatkan lebar layar monitor.
    * `screen_height = root.winfo_screenheight()`: Mendapatkan tinggi layar monitor.
    * `center_x = int(screen_width / 2 - window_width / 2)`: Menghitung posisi x agar window berada di tengah.
    * `center_y = int(screen_height / 2 - window_height / 2)`: Menghitung posisi y agar window berada di tengah.
    * `root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')`: Mengatur ukuran dan posisi window.
  * `root.mainloop()`: Memulai *event loop* Tkinter, yang membuat window tetap terbuka dan responsif terhadap interaksi pengguna.
