import mysql.connector

# Connect ke Database
db = mysql.connector.connect(
    host="localhost",
    user="DB_Admin",
    password="CRUDsql",
    database="Tugas_Project"
)

cursor = db.cursor()

## login dan registrasi 

def register():
    global cursor, db
    print("\n=== Registrasi Akun ===")
    username = input("Username: ")
    password = input("Password: ")

    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
    try:
        cursor.execute(sql, (username, password))
        db.commit()
        print("Registrasi berhasil.")
    except mysql.connector.IntegrityError:
        print("Username sudah digunakan.")

def login():
    global cursor
    print("\n=== Login ===")
    username = input("Username: ")
    password = input("Password: ")

    sql = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(sql, (username, password))
    result = cursor.fetchone()

    if result:
        print(f"Login berhasil, selamat datang {username}!")
        return True
    else:
        print("Login gagal. Username atau password salah.")
        return False

# CRUD capstone 1

def tampilkan_detail_kontak(kontak):
    print(f"ID      : {kontak[0]}")
    print(f"Nama    : {kontak[1]}")
    print(f"Company : {kontak[2]}")
    print(f"Telepon : {kontak[3]}")
    print(f"Kategori: {kontak[4]}")
    print(f"Email   : {kontak[5]}")
    print("=" * 50)

def input_telepon():
    while True:
        telepon = input("Telepon: ")
        if telepon.isdigit():
            return telepon
        else:
            print("Nomor telepon hanya boleh berisi angka.")

def konfirmasi_ya_tidak(pesan):
    while True:
        jawaban = input(pesan).lower()
        if jawaban in ['yes', 'no']:
            return jawaban
        print("Input tidak valid. Ketik 'yes' atau 'no'.")

def tambah_kontak():
    global cursor, db
    print("\n=== Tambah Kontak Baru ===")
    nama = input("Nama: ")
    company = input("Company: ")
    telepon = input_telepon()
    kategori = input("Kategori: ")
    email = input("Email: ")

    cursor.execute("SELECT * FROM kontak WHERE telepon=%s", (telepon,))
    if cursor.fetchone():
        print(f"Kontak dengan nomor '{telepon}' sudah ada.")
        return

    tampilkan_detail_kontak(("-"," + " '" + nama + "','" + company + "','" + telepon + "','" + kategori + "','" + email + "'))
    konfirmasi = konfirmasi_ya_tidak("Apakah yakin ingin menambahkan kontak ini? (yes/no): ")
    if konfirmasi == 'yes':
        sql = "INSERT INTO kontak (nama, company, telepon, kategori, email) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (nama, company, telepon, kategori, email))
        db.commit()
        print("Kontak berhasil ditambahkan.")
    else:
        print("Penambahan kontak dibatalkan.")

def tampilkan_kontak():
    global cursor
    while True:
        print("\n=== SUBMENU TAMPILKAN KONTAK ===")
        print("1. Semua Kontak Lengkap")
        print("2. Daftar Email")
        print("3. Kategori: Rekan Kerja")
        print("4. Kategori: Keluarga")
        print("5. Kategori: Teman")
        print("6. Kategori: Bisnis")
        print("7. Kembali ke Menu Utama")

        pilihan = input("Pilih submenu (1-7): ")
        kategori_dict = {'3': 'Rekan Kerja', '4': 'Keluarga', '5': 'Teman', '6': 'Bisnis'}

        if pilihan == '1':
            cursor.execute("SELECT * FROM kontak")
            hasil = cursor.fetchall()
            for kontak in hasil:
                tampilkan_detail_kontak(kontak)
        elif pilihan == '2':
            cursor.execute("SELECT id, nama, email FROM kontak")
            for kontak in cursor.fetchall():
                print(f"ID: {kontak[0]} | Nama: {kontak[1]} | Email: {kontak[2]}")
        elif pilihan in kategori_dict:
            cursor.execute("SELECT * FROM kontak WHERE kategori=%s", (kategori_dict[pilihan],))
            hasil = cursor.fetchall()
            if hasil:
                for kontak in hasil:
                    tampilkan_detail_kontak(kontak)
            else:
                print("Tidak ada kontak dalam kategori ini.")
        elif pilihan == '7':
            break
        else:
            print("Pilihan tidak valid.")

def update_kontak():
    global cursor, db
    tampilkan_kontak()
    id_kontak = input("Masukkan ID kontak yang akan diupdate: ")

    cursor.execute("SELECT * FROM kontak WHERE id=%s", (id_kontak,))
    kontak = cursor.fetchone()
    if not kontak:
        print("ID kontak tidak ditemukan.")
        return

    tampilkan_detail_kontak(kontak)
    konfirmasi = konfirmasi_ya_tidak("Yakin ingin update kontak ini? (yes/no): ")
    if konfirmasi != 'yes':
        print("Update dibatalkan.")
        return

    nama = input("Nama baru: ")
    company = input("Company baru: ")
    telepon = input("Telepon baru: ")
    kategori = input("Kategori baru: ")
    email = input("Email baru: ")

    sql = "UPDATE kontak SET nama=%s, company=%s, telepon=%s, kategori=%s, email=%s WHERE id=%s"
    cursor.execute(sql, (nama or kontak[1], company or kontak[2], telepon or kontak[3], kategori or kontak[4], email or kontak[5], id_kontak))
    db.commit()
    print("Kontak berhasil diupdate.")

def hapus_kontak():
    global cursor, db
    tampilkan_kontak()
    id_kontak = input("Masukkan ID kontak yang akan dihapus: ")

    cursor.execute("SELECT * FROM kontak WHERE id=%s", (id_kontak,))
    kontak = cursor.fetchone()
    if not kontak:
        print("ID kontak tidak ditemukan.")
        return

    tampilkan_detail_kontak(kontak)
    konfirmasi = konfirmasi_ya_tidak("Yakin ingin menghapus kontak ini? (yes/no): ")
    if konfirmasi == 'yes':
        cursor.execute("DELETE FROM kontak WHERE id=%s", (id_kontak,))
        db.commit()
        print("Kontak berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")

def cari_kontak():
    global cursor
    keyword = input("Masukkan kata kunci pencarian: ").lower()
    sql = "SELECT * FROM kontak WHERE LOWER(nama) LIKE %s OR LOWER(company) LIKE %s OR LOWER(telepon) LIKE %s OR LOWER(kategori) LIKE %s OR LOWER(email) LIKE %s"
    param = tuple([f"%{keyword}%"] * 5)
    cursor.execute(sql, param)
    hasil = cursor.fetchall()

    if hasil:
        for kontak in hasil:
            tampilkan_detail_kontak(kontak)
    else:
        print(f"Tidak ditemukan kontak dengan kata kunci '{keyword}'.")

# menu utama

def menu_utama():
    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Tampilkan Kontak")
        print("2. Tambah Kontak")
        print("3. Update Kontak")
        print("4. Hapus Kontak")
        print("5. Cari Kontak")
        print("6. Keluar")

        pilihan = input("Pilih menu (1-6): ")

        if pilihan == '1':
            tampilkan_kontak()
        elif pilihan == '2':
            tambah_kontak()
        elif pilihan == '3':
            update_kontak()
        elif pilihan == '4':
            hapus_kontak()
        elif pilihan == '5':
            cari_kontak()
        elif pilihan == '6':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid.")

# program utama

if __name__ == "__main__":
    while True:
        print("\n=== Kontak Pribadi ===")
        print("1. Login")
        print("2. Registrasi")
        print("3. Keluar")

        pilihan = input("Pilih menu (1-3): ")

        if pilihan == '1':
            if login():
                menu_utama()
        elif pilihan == '2':
            register()
        elif pilihan == '3':
            print("Terima kasih telah menggunakan Kontak Pribadi.")
            break
        else:
            print("Pilihan tidak valid.")

#{
    #     'Nama': 'Doni Pratama',
    #     'Company': 'PT Barito Satu',
    #     'Telepon': '081234567890',
    #     'Kategori': 'Rekan Kerja',
    #     'Email': 'Doni@barito.com'
    # },
    # {
    #     'Nama': 'Kania Dwi',
    #     'Company': 'PT Dentist Duo',
    #     'Telepon': '089876543210',
    #     'Kategori': 'Keluarga',
    #     'Email': 'Kaniad@gmail.com'
    # },
    # {
    #     'Nama': 'Rudi Tri Utama',
    #     'Company': 'Freelance',
    #     'Telepon': '082112345678',
    #     'Kategori': 'Teman',
    #     'Email': 'Ruditu@yahoo.com'
    # },
    # {
    #     'Nama': 'Dimas Putra',
    #     'Company': 'PT Bank Abadi',
    #     'Telepon': '081234123412',
    #     'Kategori': 'Bisnis',
    #     'Email': 'Dimasp@abadi.co.id'
    # }