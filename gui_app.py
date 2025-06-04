import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from seminar_backend import Seminar_Registration
from config import APP_SIZE

class ParticipantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Pendaftaran Seminar")
        # Ukuran jendela diatur di main.py bersamaan dengan pemusatan
        
        self.seminar_system = Seminar_Registration()
        self._setup_styles()
        self._create_widgets()
        self.refresh_table()
        if hasattr(self, 'entry_nama'): self.entry_nama.focus_set()

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        for name in ["TButton", "TLabel", "TEntry", "TCombobox"]:
            self.style.configure(name, padding=3, font=("Arial", 9))

    def _create_widgets(self):
        # Frame Utama untuk Form Input
        f_input = ttk.Frame(self.root, padding=10); f_input.pack(pady=5, padx=10, fill=tk.X)
        f_input.columnconfigure(1, weight=1)
        fields = {"Nama Lengkap:": "entry_nama", "Alamat Email:": "entry_email", "Asal Institusi:": "entry_institusi"}
        for i, (text, name) in enumerate(fields.items()):
            ttk.Label(f_input, text=text, width=15, anchor=tk.W).grid(row=i, column=0, padx=5, pady=4, sticky=tk.W)
            entry = ttk.Entry(f_input); entry.grid(row=i, column=1, padx=5, pady=4, sticky=tk.EW)
            setattr(self, name, entry) # Simpan sebagai self.entry_nama, dll.
        ttk.Button(f_input, text="Daftarkan Peserta", command=self.on_register).grid(row=len(fields), column=1, pady=8, sticky=tk.E)

        # Frame untuk Kontrol
        f_ctrl = ttk.Frame(self.root, padding=10); f_ctrl.pack(pady=5, padx=10, fill=tk.X)
        ttk.Label(f_ctrl, text="Cari Peserta:").pack(side=tk.LEFT, padx=(0,2))
        self.entry_search = ttk.Entry(f_ctrl, width=20); self.entry_search.pack(side=tk.LEFT, padx=(0,5))
        self.entry_search.bind("<Return>", self.on_search)
        ttk.Button(f_ctrl, text="Cari", command=self.on_search).pack(side=tk.LEFT, padx=(0,10))
        
        ttk.Label(f_ctrl, text="Urutkan:").pack(side=tk.LEFT, padx=(5,2))
        self.combo_sort_by = ttk.Combobox(f_ctrl, values=["Waktu Daftar", "Nama"], width=12, state="readonly")
        self.combo_sort_by.set("Waktu Daftar"); self.combo_sort_by.pack(side=tk.LEFT, padx=2)
        self.combo_sort_order = ttk.Combobox(f_ctrl, values=["Ascending", "Descending"], width=12, state="readonly")
        self.combo_sort_order.set("Ascending"); self.combo_sort_order.pack(side=tk.LEFT, padx=(2,5))
        ttk.Button(f_ctrl, text="Urutkan", command=self.on_sort).pack(side=tk.LEFT, padx=(0,5))
        ttk.Button(f_ctrl, text="Hapus", command=self.on_delete).pack(side=tk.LEFT, padx=5)

        # Frame untuk Tabel Data
        f_tbl = ttk.Frame(self.root, padding=10); f_tbl.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        cols = ("nama", "email", "institusi", "waktu_daftar")
        hdrs = ("Nama Peserta", "Alamat Email", "Asal Institusi", "Waktu Pendaftaran")
        self.tabel = ttk.Treeview(f_tbl, columns=cols, show="headings", height=10)
        w = {"nama":180, "email":220, "institusi":180, "waktu_daftar":150} # Lebar kolom
        for i, col_k in enumerate(cols):
            anchor, stretch = (tk.W, tk.YES) if col_k != "waktu_daftar" else ("center", tk.NO)
            self.tabel.heading(col_k, text=hdrs[i]); self.tabel.column(col_k, anchor=anchor, width=w[col_k], stretch=stretch)
        ys = ttk.Scrollbar(f_tbl, orient=tk.VERTICAL, command=self.tabel.yview); self.tabel.configure(yscrollcommand=ys.set); ys.pack(side=tk.RIGHT, fill=tk.Y)
        xs = ttk.Scrollbar(f_tbl, orient=tk.HORIZONTAL, command=self.tabel.xview); self.tabel.configure(xscrollcommand=xs.set); xs.pack(side=tk.BOTTOM, fill=tk.X)
        self.tabel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _format_datetime(self, dt_obj):
        return dt_obj.strftime('%Y-%m-%d %H:%M:%S') if isinstance(dt_obj, datetime) else str(dt_obj)
    
    def refresh_table(self, data_list=None):
        for item in self.tabel.get_children(): self.tabel.delete(item)
        current_data = data_list if data_list is not None \
            else self.seminar_system.sort_participants( # Ambil dari sort_participants jika None
                key={"Waktu Daftar": "waktu_daftar", "Nama": "nama"}.get(self.combo_sort_by.get(), 'waktu_daftar'),
                reverse=(self.combo_sort_order.get() == "Descending")
            )
        for p in current_data:
            self.tabel.insert("", tk.END, values=(p.get('nama',''), p.get('email',''), 
                                                p.get('institusi',''), self._format_datetime(p.get('waktu_daftar'))))
    def on_register(self):
        nama, email, inst = self.entry_nama.get(), self.entry_email.get(), self.entry_institusi.get()
        if not all([nama, email, inst]): messagebox.showwarning("Input Kurang", "Semua field harus diisi."); return
        s, msg = self.seminar_system.register_participant(nama, email, inst)
        messagebox.showinfo("Info Registrasi", msg)
        if s: self.entry_nama.delete(0,tk.END); self.entry_email.delete(0,tk.END); self.entry_institusi.delete(0,tk.END); self.refresh_table()
        
    def on_search(self, event=None):
        kw = self.entry_search.get()
        res = self.seminar_system.sequential_search(kw)
        if not res and kw: messagebox.showinfo("Info Pencarian", f"Tidak ada hasil untuk '{kw}'.")
        self.refresh_table(data_list=res)
        
    def on_sort(self): self.refresh_table() # Refresh table akan otomatis menggunakan opsi sort terpilih
    
    def on_delete(self):
        sel_id = self.tabel.focus()
        if not sel_id: messagebox.showwarning("Info Hapus", "Pilih peserta untuk dihapus."); return
        vals = self.tabel.item(sel_id)['values']
        if not vals or len(vals) < 2: messagebox.showerror("Error Data", "Data peserta tidak valid."); return
        email_del, nama_del = vals[1], vals[0]
        if messagebox.askyesno("Konfirmasi Hapus", f"Hapus '{nama_del}' ({email_del})?"):
            s, msg = self.seminar_system.delete_participant(email_del)
            messagebox.showinfo("Info Hapus", msg); self.refresh_table() # Selalu refresh setelah aksi