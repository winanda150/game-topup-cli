"""
================================================================================
Project     : Winanda Store - Game Top Up CLI
Deskripsi   : Aplikasi CLI simulasi transaksi top up game online & manajemen akun
Penulis     : I Wayan Winanda
Bahasa      : Python 3
================================================================================
"""

# ==============================================================================
# DEPENDENCIES & MODUL STANDAR
# ==============================================================================
import getpass
import os
import time

# ==============================================================================
# KONFIGURASI GLOBAL & KATALOG PRODUK
# ==============================================================================

# Banner ucapan selamat datang pada menu awal
banner = (
    "===== Selamat Datang di Winanda Store =====\n"
    "Pilih Opsi Berikut :\n"
    "1. Login\n"
    "2. Register"
)

# Daftar kategori game yang tersedia untuk layanan top up
listproduk = [
    "Top Up Mobile Legends",
    "Top Up Free Fire Max",
    "Top Up Super Sus",
    "Top Up Call Of Duty Mobile"
]

# Dictionary penampung data sesi transaksi aktif
dict_trx = {}

# Daftar metode pembayaran yang didukung
metode_pembayaran = {
    1: "Qris",
    2: "Kartu Kredit",
    3: "Virtual Account",
    4: "Bank Transfer",
}

# Daftar pengguna dengan hak akses khusus (Admin)
list_admin = {
    1: "Winanda",
    2: "Reva",
    3: "Gustadi",
}

# ------------------------------------------------------------------------------
# Daftar Harga Produk (Mapping ID Opsi -> Harga dalam IDR)
# ------------------------------------------------------------------------------

# Harga Top Up Mobile Legends: Bang Bang (WDP, Pass & Diamonds)
hargatopupmlbb = {
    1: 26000,
    2: 78000,
    3: 130000,
    4: 150000,
    5: 1500,
    6: 12000,
    7: 22000,
    8: 44000,
    9: 76000,
    10: 105000,
    11: 143000,
    12: 219000,
    13: 475000
}

# Harga Top Up Free Fire Max (Diamonds)
hargatopupff = {
    1: 1500,
    2: 10000,
    3: 20000,
    4: 45000,
    5: 90000,
    6: 180000,
    7: 270000,
    8: 450000
}

# Harga Top Up Super Sus (Goldstar & Subscription Passes)
hargatopupsus = {
    1: 10000,
    2: 35000,
    3: 57000,
    4: 117000,
    5: 240000,
    6: 613000,
    7: 73000,
    8: 128000,
    9: 13000,
    10: 134000,
    11: 157000
}

# Harga Top Up Call of Duty: Mobile (CP - COD Points)
hargatopupcodm = {
    1: 10000,
    2: 18000,
    3: 45000,
    4: 90000,
    5: 180000,
    6: 270000,
    7: 450000,
    8: 900000
}


# ==============================================================================
# AUTENTIKASI & ALUR UTAMA (CORE FLOW)
# ==============================================================================

def main():
    """
    Menampilkan menu pembuka aplikasi serta mengarahkan pengguna
    ke alur Login atau Registrasi akun baru.
    """
    print(banner)
    while True:
        try:
            opsi = int(input("Opsi : "))
        except ValueError:
            print("Masukkan angka 1 atau 2!")
            continue

        if opsi == 1:
            time.sleep(1)
            login()
            break
        elif opsi == 2:
            time.sleep(1)
            register()
            break
        else:
            print("Pilihan tidak tersedia, coba lagi!")


def login():
    """
    Menangani proses verifikasi login pengguna berdasarkan username
    dan kata sandi yang tersimpan di basis data file (Akun.txt).
    """
    print("========= Login di Winanda Store ==========")
    username = input("Masukkan username : ")
    cekuser = False

    # Verifikasi keberadaan username di file database
    try:
        with open("Akun.txt", "r") as file:
            for cek in file:
                user, _ = cek.strip().split(",")
                if user == username:
                    cekuser = True
                    break
    except FileNotFoundError:
        pass

    if not cekuser:
        print(f"Username {username} belum terdaftar")
        main()
        return

    password = getpass.getpass("Masukkan Kata Sandi : ")
    print("Loading...")
    time.sleep(4)

    # Validasi kombinasi username dan password
    verifikasi = False
    try:
        with open("Akun.txt", "r") as file:
            for line in file:
                user, pwd = line.strip().split(",")
                if user == username and pwd == password:
                    verifikasi = True
                    break
    except FileNotFoundError:
        pass

    if verifikasi:
        print("Login berhasil...")
        time.sleep(2)
        print("Selamat datang di Winanda Store!")
        print(f"Username : {username}")
        menu(username)
    else:
        print("Password yang anda masukkan salah. Silahkan coba lagi!")
        main()
        return


def register():
    """
    Mendaftarkan pengguna baru dengan melakukan pengecekan ketersediaan
    username, konfirmasi kata sandi, dan menyimpannya ke Akun.txt.
    """
    print("========= Register di Winanda Store ==========")
    username = input("Masukkan username : ")

    # Pengecekan apakah username sudah digunakan sebelumnya
    cekuser = False
    try:
        with open("Akun.txt", "r") as file:
            for cek in file:
                user, _ = cek.strip().split(",")
                if user == username:
                    cekuser = True
                    break
    except FileNotFoundError:
        pass

    if cekuser:
        print("Username sudah digunakan, silahkan pilih yang lain.")
        main()
        return

    password = getpass.getpass("Masukkan Kata Sandi : ")
    confirm = getpass.getpass("Konfirmasi Kata Sandi : ")
    print("Loading...")
    time.sleep(5)

    # Validasi kesesuaian konfirmasi password
    if password != confirm:
        print("Password tidak sama, registrasi dibatalkan.")
        main()
        return

    # Menyimpan kredensial akun baru ke file Akun.txt
    with open("Akun.txt", "a") as file:
        file.write(f"{username},{password}\n")

    print("Register Telah Berhasil! Silahkan Login.")
    time.sleep(2)
    main()
    return


def menu(username):
    """
    Menampilkan dasbor menu utama setelah pengguna berhasil login,
    termasuk navigasi top up game, logout, penghapusan akun, serta
    menu khusus jika pengguna memiliki hak akses Admin.
    """
    print("===== Top Up Winanda Store =====")
    print("Silahkan pilih jenis top up berikut :")
    print("1. Top Up Game")
    print("2. Logout")
    print("3. Hapus Akun")
    
    # Opsi khusus jika pengguna terdaftar sebagai admin
    if username in list_admin.values():
        print("4. Menu Admin")

    while True:
        try:
            if username in list_admin.values():
                idproduk = int(input("Pilih produk (1-4): "))
            else:
                idproduk = int(input("Pilih produk (1-3): "))
        except ValueError:
            if username in list_admin.values():
                print("Masukkan angka 1 - 4!")
            else:
                print("Masukkan angka 1 - 3!")
            continue

        if idproduk == 1:
            time.sleep(2)
            topupgame(username)
            break
        elif idproduk == 2:
            time.sleep(2)
            print(f"Anda telah logout dari Akun username {username}")
            time.sleep(2)
            main()
            break
        elif idproduk == 3:
            time.sleep(2)
            hapus_akun(username)
            break
        elif idproduk == 4 and username in list_admin.values():
            time.sleep(2)
            admin_menu(username)
            break
        else:
            print("Pilihan tidak tersedia, coba lagi!")


# ==============================================================================
# MENU & FITUR KHUSUS ADMIN
# ==============================================================================

def admin_menu(username):
    """
    Menampilkan panel manajemen khusus administrator untuk memonitor
    seluruh daftar akun terdaftar maupun daftar admin.
    """
    print("===== Menu Admin Winanda Store =====")
    print("1. Lihat Semua Akun")
    print("2. Kembali ke Menu Utama")
    print("3. Lihat Akun Admin")

    while True:
        try:
            pilih = int(input("Masukkan pilihan anda : "))
        except ValueError:
            print("Masukkan angka 1 - 3!")
            continue

        if pilih == 1:
            time.sleep(1)
            lihatakun(username)
            break
        elif pilih == 2:
            time.sleep(1)
            menu(username)
            break
        elif pilih == 3:
            time.sleep(1)
            lihatadmin(username)
            break
        else:
            print("Opsi tidak tersedia, coba lagi!")


def lihatakun(username):
    """
    Membaca dan menampilkan seluruh username akun yang terdaftar pada sistem.
    """
    try:
        with open("Akun.txt", "r") as file:
            print("Akun Terdaftar :")
            for i in file:
                user = i.strip().split(",")[0]
                print(f"Username : {user}")

        opsi = input("Apakah anda ingin kembali ke menu admin? (Y) : ")
        if opsi.lower() == "y":
            admin_menu(username)
            return
        else:
            print("Opsi tidak tersedia, coba lagi!")
    except FileNotFoundError:
        print("Akun tidak ditemukan")


def lihatadmin(username):
    """
    Menyaring dan menampilkan akun terdaftar yang memiliki hak istimewa sebagai Admin.
    """
    try:
        with open("Akun.txt", "r") as file:
            print("Akun Admin Terdaftar :")
            for i in file:
                user = i.strip().split(",")[0]
                if user in list_admin.values():
                    print(f"Username : {user}")

        opsi = input("Apakah anda ingin kembali ke menu admin? (Y) : ")
        if opsi.lower() == "y":
            admin_menu(username)
            return
        else:
            print("Opsi tidak tersedia, coba lagi!")
    except FileNotFoundError:
        print("Akun tidak ditemukan")


# ==============================================================================
# KATALOG & ALUR TOP UP GAME
# ==============================================================================

def topupgame(username):
    """
    Menampilkan daftar pilihan game yang tersedia dan mengarahkan pengguna
    ke form pemesanan spesifik sesuai game yang dipilih.
    """
    print("===== Winanda Store =====")
    print("Silahkan pilih jenis top up game berikut :")
    for id, produk in enumerate(listproduk, 1):
        print(f"{id}. {produk}")

    while True:
        try:
            produkid = int(input("Masukkan jenis top up (1-4) : "))
        except ValueError:
            print("Masukkan angka 1 - 4!")
            continue

        dict_trx["produkid"] = produkid

        if produkid == 1:
            time.sleep(2)
            mlbb(username)
            break
        elif produkid == 2:
            time.sleep(2)
            ffmax(username)
            break
        elif produkid == 3:
            time.sleep(2)
            sus(username)
            break
        elif produkid == 4:
            time.sleep(2)
            codm(username)
            break
        else:
            print("Pilihan tidak tersedia, coba lagi!")


def mlbb(username):
    """
    Menangani alur transaksi Top Up Mobile Legends: Bang Bang.
    Mengumpulkan input User ID, Zone ID, paket Diamond/Pass, dan kuantitas pembelian.
    """
    print("===== Selamat Datang di Top Up Mobile Legends =====")
    print("1. Masukkan User ID")

    # Input dan validasi User ID serta Zone ID
    while True:
        try:
            idmlbb = int(input("Masukkan Id ML : "))
            zonemlbb = int(input("Masukkan Id Zone : "))
        except ValueError:
            print("Masukkan angka!")
            continue

        dict_trx["idmlbb"] = idmlbb
        dict_trx["zonemlbb"] = zonemlbb
        break

    time.sleep(1)
    print("2. Pilih Nominal Top Up")
    print("===== Weekly Diamond Pass =====")
    wdp = [
        "1. 1x Weekly Diamond Pass",
        "2. 3x Weekly Diamond Pass",
        "3. 5x Weekly Diamond Pass",
        "4. Twilight Pass",
    ]
    for item in wdp:
        print(item)

    time.sleep(1)
    print("=========== Diamond ===========")
    dm = [
        "5. 5 Diamond",
        "6. 44 Diamond",
        "7. 85 Diamond",
        "8. 170 Diamond",
        "9. 296 Diamond",
        "10. 408 Diamond",
        "11. 568 Diamond",
        "12. 875 Diamond",
        "13. 2010 Diamond",
    ]
    for item in dm:
        print(item)

    all_produkmlbb = wdp + dm

    # Pemilihan paket nominal produk
    while True:
        try:
            opsi1 = int(input("Masukkan id produk : "))
        except ValueError:
            print("Masukkan angka, bukan teks!")
            continue

        if 1 <= opsi1 <= len(all_produkmlbb):
            dict_trx["opsi1"] = opsi1
            break
        else:
            print("id produk tidak tersedia, silahkan coba lagi!")
    
    print("===========================")
    time.sleep(1)
    print("3. Pilih Jumlah Pembelian")

    # Validasi kuantitas pembelian (1-10)
    while True:
        try:
            jumlah = int(input("Masukkan jumlah pembelian (1-10): "))
        except ValueError:
            print("Masukkan angka, bukan teks!")
            continue

        if 1 <= jumlah <= 10:
            dict_trx["jumlah"] = jumlah
            break
        else:
            print("Jumlah produk telah maksimum, silahkan coba lagi!")

    metodepembayaran(hargatopupmlbb, all_produkmlbb, username)


def ffmax(username):
    """
    Menangani alur transaksi Top Up Free Fire Max.
    Mengumpulkan input Player ID, pilihan Diamond, dan kuantitas pembelian.
    """
    print("===== Selamat Datang di Top Up Free Fire Max =====")
    print("1. Masukkan Player ID")

    # Input dan validasi Player ID
    while True:
        try:
            idff = int(input("Masukkan Id FF : "))
        except ValueError:
            print("Masukkan angka, bukan teks")
            continue

        dict_trx["idff"] = idff
        break

    time.sleep(1)
    print("2. Pilih Nominal Top Up")
    print("======= Diamond =======")
    dmff = [
        "1. 5 Diamond",
        "2. 50 Diamond",
        "3. 140 Diamond",
        "4. 355 Diamond",
        "5. 720 Diamond",
        "6. 1450 Diamond",
        "7. 2180 Diamond",
        "8. 3640 Diamond",
    ]
    for item in dmff:
        print(item)

    all_produkff = dmff

    # Pemilihan paket nominal Diamond
    while True:
        try:
            opsi1 = int(input("Masukkan id produk : "))
        except ValueError:
            print("Masukkan angka, bukan teks!")
            continue

        if 1 <= opsi1 <= len(all_produkff):
            dict_trx["opsi1"] = opsi1
            break
        else:
            print("id produk tidak tersedia, silahkan coba lagi!")
    
    print("===========================")
    time.sleep(1)
    print("3. Pilih Jumlah Pembelian")

    # Validasi kuantitas pembelian (1-10)
    while True:
        try:
            jumlah = int(input("Masukkan jumlah pembelian (1-10): "))
        except ValueError:
            print("Masukkan angka, bukan teks!")
            continue

        if 1 <= jumlah <= 10:
            dict_trx["jumlah"] = jumlah
            break
        else:
            print("Jumlah produk telah maksimum, silahkan coba lagi!")

    metodepembayaran(hargatopupff, all_produkff, username)


def sus(username):
    """
    Menangani alur transaksi Top Up Super Sus.
    Mengumpulkan input ID Space, pilihan Goldstar/Pass, dan kuantitas pembelian.
    """
    print("===== Selamat Datang di Top Up Super Sus =====")
    print("1. Masukkan ID Space")

    # Input dan validasi ID Space
    while True:
        try:
            idsus = int(input("Masukkan Id Space : "))
        except ValueError:
            print("Masukkan angka, bukan teks")
            continue

        dict_trx["idsus"] = idsus
        break

    time.sleep(1)
    print("2. Pilih Nominal Top Up")
    print("======= Diamond =======")
    dmsus = [
        "1. 100 Goldstar",
        "2. 310 Goldstar",
        "3. 520 Goldstar",
        "4. 1060 Goldstar",
        "5. 2180 Goldstar",
        "6. 5600 Goldstar",
        "7. Super Pass",
        "8. Super Pass Bundle",
        "9. Weekly Card",
        "10. Monthly Card",
        "11. Super VIP Card",
    ]
    for Goldstart in dmsus:
        print(Goldstart)

    all_produksus = dmsus

    # Pemilihan paket nominal Goldstar atau Pass
    while True:
        try:
            opsi1 = int(input("Masukkan id produk : "))
        except ValueError:
            print("Masukkan angka, bukan teks!")
            continue

        if 1 <= opsi1 <= len(all_produksus):
            dict_trx["opsi1"] = opsi1
            break
        else:
            print("id produk tidak tersedia, silahkan coba lagi!")
    
    print("===========================")
    time.sleep(1)
    print("3. Pilih Jumlah Pembelian")

    # Validasi kuantitas pembelian (1-10)
    while True:
        try:
            jumlah = int(input("Masukkan jumlah pembelian (1-10): "))
        except ValueError:
            print("Masukkan angka, bukan teks!")
            continue

        if 1 <= jumlah <= 10:
            dict_trx["jumlah"] = jumlah
            break
        else:
            print("Jumlah produk telah maksimum, silahkan coba lagi!")

    metodepembayaran(hargatopupsus, all_produksus, username)


def codm(username):
    """
    Menangani alur transaksi Top Up Call of Duty: Mobile.
    Mengumpulkan input PlayerID, paket CP (COD Points), dan kuantitas pembelian.
    """
    print("===== Selamat datang di Top Up Call Of Duty Mobile =====")
    print("1. Masukkan PlayerID")

    # Input dan validasi PlayerID
    while True:
        try:
            idcodm = int(input("Masukkan PlayerID : "))
        except ValueError:
            print("Masukkan angka, bukan teks!")
            continue

        dict_trx["idcodm"] = idcodm
        break

    time.sleep(1)
    print("2. Pilih Nominal Top Up")
    print("======= CP =======")
    cpcodm = [
        "1. 63 CP",
        "2. 128 CP",
        "3. 321 CP",
        "4. 645 CP",
        "5. 1373 CP",
        "6. 2060 CP",
        "7. 3564 CP",
        "8. 7656 CP",
    ]
    for CP in cpcodm:
        print(CP)

    allprodukcodm = cpcodm

    # Pemilihan paket nominal CP
    while True:
        try:
            opsi1 = int(input("Masukkan id produk : "))
        except ValueError:
            print("Masukkan angka, bukan teks!")
            continue

        if 1 <= opsi1 <= len(allprodukcodm):
            dict_trx["opsi1"] = opsi1
            break
        else:
            print("id produk tidak tersedia, silahkan coba lagi")
    
    print("===========================")
    time.sleep(1)
    print("3. Pilih Jumlah Pembelian")

    # Validasi kuantitas pembelian (1-10)
    while True:
        try:
            jumlah = int(input("Masukkan jumlah pembelian (1-10): "))
        except ValueError:
            print("Masukkan angka, bukan teks!")
            continue

        if 1 <= jumlah <= 10:
            dict_trx["jumlah"] = jumlah
            break
        else:
            print("Jumlah produk telah maksimum, silahkan coba lagi!")

    metodepembayaran(hargatopupcodm, allprodukcodm, username)


# ==============================================================================
# MANAJEMEN AKUN (PENGHAPUSAN AKUN)
# ==============================================================================

def hapus_akun(username):
    """
    Menghapus akun pengguna yang sedang aktif dari file penyimpanan Akun.txt
    setelah mendapatkan konfirmasi eksplisit dari pengguna.
    """
    print("===== Hapus Akun Winanda Store =====")
    while True:
        konfirmasi = input(f"Apakah Anda yakin ingin menghapus akun {username}? (Y/N): ")
        if konfirmasi.lower() == "y":
            try:
                with open("Akun.txt", "r") as f:
                    lines = f.readlines()
                with open("Akun.txt", "w") as f:
                    for line in lines:
                        if not line.startswith(username + ","):
                            f.write(line)
                print("Akun berhasil dihapus.")
            except FileNotFoundError:
                print("Data akun tidak ditemukan.")
            main()
            break
        elif konfirmasi.lower() == "n":
            print("Anda membatalkan penghapusan akun")
            time.sleep(2)
            menu(username)
            break
        else:
            print("Input tidak valid. Silakan masukkan Y atau N.")

# ==============================================================================
# PEMBAYARAN, RINCIAN STRUK & CHECKOUT
# ==============================================================================

def metodepembayaran(harga_dict, produk_list, username):
    """
    Menangani alur checkout: pemilihan metode pembayaran, kalkulasi biaya (subtotal,
    biaya admin/pajak, total), menampilkan invoice pesanan, dan konfirmasi transaksi.
    
    Parameters:
        harga_dict (dict): Dictionary mapping opsi produk ke harga satuan.
        produk_list (list): Daftar nama/label produk yang dipilih.
        username (str): Username pembeli yang sedang aktif.
    """
    print("===========================")
    time.sleep(1)
    print("4. Pilih Metode Pembayaran")
    for id, name in metode_pembayaran.items():
        print(f"{id}. {name}")

    # Validasi opsi metode pembayaran
    while True:
        try:
            pembayaran = int(input("Masukkan metode pembayaran (1-4): "))
        except ValueError:
            print("Masukkan angka, bukan teks!")
            continue

        if 1 <= pembayaran <= len(metode_pembayaran):
            dict_trx["pembayaran"] = pembayaran
            break
        else:
            print("Metode Pembayaran tidak tersedia, silahkan coba lagi!")

    print("Loading...")
    time.sleep(3)

    # Kalkulasi rincian harga dan biaya administrasi
    produk_nama = produk_list[dict_trx['opsi1'] - 1].split('. ', 1)[-1]
    jumlah = dict_trx.get("jumlah", 1)
    harga_satuan = harga_dict[dict_trx["opsi1"]]
    total = harga_satuan * jumlah

    # Biaya administrasi / penanganan berdasarkan metode pembayaran
    pajak_persen = {
        1: 850,   # QRIS (Biaya Penanganan Tetap)
        2: 2050,  # Kartu Kredit
        3: 2550,  # Virtual Account
        4: 1500   # Bank Transfer
    }
    pajak = pajak_persen.get(pembayaran, 0)
    nama_produk = listproduk[dict_trx["produkid"] - 1]

    # Menampilkan struk rincian pesanan
    print("======= Detail Pesanan =======")
    print(f"Top Up : {nama_produk.replace('Top Up ', '')}")
    print(f"Username : {username}")

    # Menampilkan ID game sesuai dengan produk yang dipilih
    if "idmlbb" in dict_trx:
        print(f"User Id : {dict_trx['idmlbb']}")
    if "zonemlbb" in dict_trx:
        print(f"ID Zone : {dict_trx['zonemlbb']}")
    if "idff" in dict_trx:
        print(f"User Id : {dict_trx['idff']}")
    if "idsus" in dict_trx:
        print(f"User Id : {dict_trx['idsus']}")
    if "idcodm" in dict_trx:
        print(f"User Id : {dict_trx['idcodm']}")

    print(f"Produk : {produk_nama}")
    print(f"Jumlah Pembelian : {jumlah} Produk")
    print(f"Metode Pembayaran : {metode_pembayaran[pembayaran]}")
    print(f"Harga Satuan : Rp {harga_satuan:,}")
    print(f"Subtotal : Rp {total:,}")
    print(f"Pajak : Rp {pajak:,}")
    print(f"Total Pembayaran : Rp {total + pajak:,}")
    print("=================================")

    time.sleep(1)

    # Konfirmasi akhir transaksi
    while True:
        konfirmasi = input("Apakah anda yakin dengan data tersebut? (Y/N): ")
        if konfirmasi.lower() == "y":
            print("Memproses transaksi...")
            time.sleep(6)
            print("Transaksi berhasil!")
            print("Silahkan cek akun anda untuk melihat top up yang sudah masuk")
            print("Terima kasih telah bertransaksi di Winanda Store!")
            dict_trx.clear()
            break
        elif konfirmasi.lower() == "n":
            time.sleep(3)
            print("Anda membatalkan transaksi")
            dict_trx.clear()
            menu(username)
            return
        else:
            print("Input tidak valid. Silakan masukkan Y atau N.")


# ==============================================================================
# ENTRY POINT PROGRAM
# ==============================================================================

if __name__ == "__main__":
    os.system("cls")
    main()