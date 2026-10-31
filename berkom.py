'''
Author              : Kelompok 5
Tanggal Pengerjaan  : 19-25 Oktober 2026

PROGRAM TemuIn - Pencari barang hilang
Deskripsi           : Simulasi sistem Lost And Found lingkungan ITB dengan fitur-fitur berupa pelaporan, pencarian, pengaduan
                      barang hilang, melihat list barang dan aduan, serta konfirmasi barang telah dikembalikan.

KAMUS
nama_lengkap            = variabel penyimpan nama lengkap pengguna
nim                     = variabel penyimpan NIM pengguna
kontak                  = variabel penyimpan kontak pengguna
list_barang             = dictionary penyimpan data barang hilang
list_aduan              = dictionary penyimpan data aduan barang hilang
mencari_barang          = fungsi pencarian barang
kategori                = list kategori barang yang dicari atau dilaporkan
kategori_hilang         = variabel penyimpan kategori barang yang ditemukan
Ini cara buat bikin autocompleter ya, misal list nya itu:
x = ['ayam', 'apel', 'babi', 'bebek']
y = WordCompleter(x, ignore_case = True)
input = prompt("Masuk sini: ", completer = y)
'''
import os
import subprocess
import sys
import csv
import time
import shutil
import uuid
import pandas as pd
from datetime import datetime
from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from math import ceil

kategori = ['Elektronik', 'ATK', 'Dompet', 'Kartu', 'Pakaian & Aksesoris', 'Kunci', 'Alat Ibadah', 'Wadah Konsumsi']
loc_ambil = ['GKU 1', 'GKU 2', 'GKU 3', 'Gedung A/E', 'Gedung Utama', 'Sekretariat Ditsama']
# Deklarasi variabel global
list_barang = pd.read_csv("pelaporan.csv")
list_aduan = pd.read_csv("pengaduan.csv")
list_barang.index += 1
list_aduan.index += 1
nama_lengkap = None
nim = None
kontak = None
data_pelaporan = []
data_pengaduan = []

def typing_effect(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def generate_id(list_data, mode):
    prefix = ""
    if (mode == "Pelaporan"):
        prefix = 'L'
    else:
        prefix = 'A'

    id = (prefix + str(uuid.uuid1())[0:5]).upper()
    while ((list_data['ID'] == id).any()):
        id = (prefix + str(uuid.uuid1())[0:5]).upper()

    return id

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def pindah_menu():
    typing_effect('\nAnda akan dialihkan ke menu berikutnya...')
    time.sleep(2)
    bersihkan_layar()

def pilih_autofill(pesan, pilihan):
    if not pilihan:
        return None
    typing_effect('\nPilihan yang tersedia:')
    for nomor, opsi in enumerate(pilihan, start=1): #iterasi skaligus beri indeks di tiap elemen
        print(f'{nomor}. {opsi}')
    daftar_saran= WordCompleter(pilihan, ignore_case=True) #ignore kapital
    while True:
        input_pilihan = prompt(pesan, completer = daftar_saran).strip() #menghapus spasi
        for opsi in pilihan:
            if input_pilihan.casefold()== opsi.casefold():
                return opsi
        #di luar for karena return pasti stop
        print("Pilihan tidak tersedia. Silakan pilih dari daftar yang disediakan.")

def detail_barang(barang, mode):
    #tampilin detail dari barang yang dipilih
    pindah_menu()
    print('=== DETAIL BARANG ===')

    print(f"ID                  : {barang['ID']}")
    print(f"Nama barang         : {barang['keyword']}")
    print(f"Kategori            : {barang['kategori']}")
    print(f"Deskripsi           : {barang['deskripsi']}")
    print(f"Waktu ditemukan     : {barang['waktu']}")
    print(f"Lokasi ditemukan    : {barang['loc_found']}")
    print(f"Lokasi pengambilan  : {barang['loc_pick']}")
    if mode == "pelaporan":
        file_foto = os.path.join("gambar_pelaporan", barang['path_gambar'])
    else:
        file_foto = os.path.join("gambar_pengaduan", barang['path_gambar'])
    os.startfile(file_foto)

def input_waktu(pesan):
    format = "%d/%m/%y %H.%M"
    while True:
        waktu_user = input(pesan).strip()
        try:
            waktu_valid = datetime.strptime(waktu_user, format)
            return waktu_valid.strftime(format)
        except ValueError:
            typing_effect("Format salah! Pastikan menggunakan format 'dd/mm/yy HH.MM'!")

def input_gambar(id, csv_path, folder_tujuan):
    os.makedirs(folder_tujuan, exist_ok=True)
    while True:
        foto = input("Drag and Drop gambar Anda dan klik Enter!").strip('\'" ')
        if foto and os.path.exists(foto):
            break
        else:
            print("Gambar tidak valid, silahkan input ulang.")
    jumlah_baris = 0
    with open(csv_path, mode='r', encoding='utf-8') as f:
        for line in f:
            jumlah_baris += 1
    ekstensi = os.path.splitext(foto)[1]
    nama_csv = csv_path.split(".")[0]
    waktu = datetime.now()
    nama_waktu = waktu.strftime("%Y%m%d_%H%M%S")
    nama_foto = f"foto_{nama_csv}_{id}{ekstensi}"
    foto_temuan = os.path.join(f"{folder_tujuan}", nama_foto)
    shutil.copy(foto, foto_temuan)
    return foto_temuan

def pengaduan_barang(nama_lengkap, nim, kontak):
    pindah_menu()
    typing_effect("=== PENGADUAN BARANG HILANG ===")
    kategori_aduan = pilih_autofill("Apa kategori barang yang Anda temukan? ", kategori)
    typing_effect("Berikan keyword dari barang yang Anda ingin adukan.\nPetunjuk : Gunakan Format 'Jenis Barang' + 'Merk atau warna'\nContoh : 'Laptop Lenovo', 'Jaket Hitam'")
    id_aduan = generate_id(list_aduan, "Pengaduan")
    keyword_aduan = input("Masukkan keyword: ")
    deskripsi_aduan = input("Berikan deskripsi dari barang yang Anda adukan: ")
    waktu_aduan = input_waktu("Masukkan waktu barang diadukan (dd/mm/yy HH.MM): ")
    lokasi_aduan = input("Dimana barang ini ditemukan? ")
    foto_aduan = input_gambar(id_aduan, "pengaduan.csv", "gambar_pengaduan")   
    # List sementara barang hilang yang akan ditambahkan ke dataframe list_barang
    data_pengaduan.append([nama_lengkap, nim, kontak, id_aduan,kategori_aduan, keyword_aduan, 
                               deskripsi_aduan, waktu_aduan, lokasi_aduan])
    typing_effect(f"Laporan sudah masuk di {datetime.now()}!")
    time.sleep(2)
    typing_effect("Terima kasih atas Aduannya! Semoga cepat ketemu ya :)")
    pindah_menu()

def pencarian_barang():
    pindah_menu()
    typing_effect('=== PENCARIAN BARANG HILANG ===')

    data = pd.read_csv('pelaporan.csv', dtype=str).fillna('') #ubah nilai kosong dengan string "" agar saat casefold tidak error
    if data.empty:
        print('Belum ada barang yang dilaporkan.')
        pindah_menu()
        return

    kategori_dicari = pilih_autofill('Kategori barang yang dicari: ', kategori)
    hasil_kategori = data[
        #ambil kolom kategori, dicocokkan dengan kategori yg dicari, menghasilkan True/False --> diambil true
        data['kategori'].str.casefold() == kategori_dicari.casefold()
    ]

    if hasil_kategori.empty:
        print('Belum ada barang dengan kategori tersebut.')
        pindah_menu()
        return #menghentika fungsi pencarian barang

    #saran keyword diambil dari barang pada kategori yang dipilih
    daftar_keyword = hasil_kategori['keyword'].drop_duplicates().tolist()
    saran = WordCompleter(daftar_keyword, ignore_case=True, sentence=True)
    keyword = prompt('Kata kunci barang: ', completer=saran).strip()

    if keyword == '':
        print('Kata kunci tidak boleh kosong.')
        pindah_menu()
        return
    
    hasil = hasil_kategori[
        hasil_kategori['keyword'].str.contains(keyword, case=False, regex=False)
    ]
    if hasil.empty:
        print('Barang belum ditemukan. Silakan coba kata kunci lain atau buat pengaduan.')
        pindah_menu()
        return

    #pakai indeks asli dataframe biar barang yang dipilih tidak tertukar
    print('\n=== HASIL PENCARIAN ===')
    for nomor, (_, barang) in enumerate(hasil.iterrows(), start=1):
        kode = barang['ID'] if 'ID' in hasil.columns else '-'
        print(f"{nomor}. ID: {kode} | {barang['keyword']} | {barang['deskripsi']}")

    while True:
        pilihan = input('Pilih nomor barang (0 untuk kembali): ').strip()
        if not pilihan.isdigit():
            print('Masukkan angka yang valid.')
            continue
        pilihan = int(pilihan)
        if pilihan == 0:
            pindah_menu()
            return
        if 1 <= pilihan <= len(hasil):
            break
        print('Nomor barang tidak tersedia.')

    barang = hasil.iloc[pilihan - 1]
    pindah_menu()
    print('=== DETAIL BARANG ===')
    if 'ID' in hasil.columns:
        print(f"ID                  : {barang['ID']}")
        
    print(f"Nama barang         : {barang['keyword']}")
    print(f"Kategori            : {barang['kategori']}")
    print(f"Deskripsi           : {barang['deskripsi']}")
    print(f"Waktu ditemukan     : {barang['waktu']}")
    print(f"Lokasi ditemukan    : {barang['loc_found']}")
    print(f"Lokasi pengambilan  : {barang['loc_pick']}")
    os.startfile()

    while True:
        yakin = input('Apakah ini barang yang Anda cari? (ya/tidak): ').strip().casefold()
        if yakin == 'ya':
            print('\nBarang yang Anda cari mungkin sudah ditemukan.')
            print(f"Silakan datang ke {barang['loc_pick']} dan membawa KTM.")
            print('Petugas akan memeriksa kepemilikan barang.')
            print('Setelah pengambilan, mintalah informasi NIM pelapor kepada petugas')
            print('untuk konfirmasi status pada opsi menu 6.')
            break
        if yakin == 'tidak':
            print('Silakan mencoba pencarian kembali melalui menu utama.')
            break
        print("Masukkan 'ya' atau 'tidak'.")

    pindah_menu()
 
def pelaporan_barang(nama_lengkap, nim, kontak):
    pindah_menu()
    typing_effect("=== PELAPORAN BARANG TEMUAN ===")
    kategori_temuan = pilih_autofill("Apa kategori barang yang Anda temukan? ", kategori)
    typing_effect("Berikan keyword dari barang yang Anda temukan.\nPetunjuk : Gunakan Format 'Jenis Barang' + 'Merk atau warna'\nContoh : 'Laptop Lenovo', 'Jaket Hitam'")
    id_temuan = generate_id(list_barang, "Pelaporan")
    keyword_temuan = input("Masukkan keyword: ")
    deskripsi_temuan = input("Berikan deskripsi dari barang yang Anda temukan: ")
    waktu_temuan = input_waktu("Masukkan waktu barang ditemukan (dd/mm/yy HH.MM): ")
    lokasi_temuan = input("Dimana barang ini ditemukan? ")
    foto_temuan = input_gambar(id_temuan, "pelaporan.csv", "gambar_pelaporan")   
    lokasi_pengambilan = pilih_autofill("Pilih salah satu lokasi berikut untuk menitipkan barang: ", loc_ambil)
    # List sementara barang hilang yang akan ditambahkan ke dataframe list_barang
    data_pelaporan.append([nama_lengkap, nim, kontak, id_temuan,kategori_temuan, keyword_temuan, 
                           deskripsi_temuan, waktu_temuan, lokasi_temuan, lokasi_pengambilan])
    typing_effect(f"Laporan sudah masuk di {datetime.now()}!")
    time.sleep(1)
    typing_effect("Terima kasih atas laporannya! Semoga bermanfaat ya :)")
    pindah_menu()

def konfirmasi_status():
    pindah_menu()
    typing_effect('=== KONFIRMASI STATUS BARANG ATAU ADUAN ===')
    print('1. Konfirmasi pelaporan barang temuan')
    print('2. Konfirmasi pengaduan barang hilang')
    print('0. Kembali ke menu utama')

    while True:
        jenis = input('Pilih menu: ').strip()
        if jenis in ('0', '1', '2'):
            break
        print('Pilihan tidak tersedia.')

    if jenis == '0':
        pindah_menu()
        return

    file = 'pelaporan.csv' if jenis == '1' else 'pengaduan.csv'
    data = pd.read_csv(file, dtype=str).fillna('')
    if data.empty:
        print('Belum ada data yang bisa dikonfirmasi.')
        pindah_menu()
        return

    #tetap bisa berjalan jika csv lama belum punya kolom id
    print('\n=== DAFTAR DATA ===')
    for nomor, (_, baris) in enumerate(data.iterrows(), start=1):
        kode = baris['ID'] if 'ID' in data.columns else '-'
        print(f"{nomor}. ID: {kode} | {baris['keyword']} | {baris['kategori']}")

    while True:
        nomor = input('Pilih nomor data yang ingin dikonfirmasi (0 untuk kembali): ').strip()
        if not nomor.isdigit():
            print('Masukkan angka yang valid.')
            continue
        nomor = int(nomor)
        if nomor == 0:
            pindah_menu()
            return
        if 1 <= nomor <= len(data):
            break
        print('Nomor data tidak tersedia.')

    #iloc memakai posisi baris, jadi nomor tampilan dikurangi satu
    posisi = nomor - 1
    nim_asli = data.iloc[posisi]['nim'].strip()
    benar = False

    #tiga kali kesempatan input nim
    for percobaan in range(3):
        nim_input = input('Masukkan NIM pelapor/pengadu: ').strip()
        if nim_input == nim_asli:
            benar = True
            break
        sisa = 2 - percobaan
        if sisa > 0:
            print(f'NIM tidak cocok. Kesempatan tersisa: {sisa}')

    if not benar:
        print('Batas percobaan telah tercapai.')
        pindah_menu()
        return

    while True:
        yakin = input('Apakah Anda yakin ingin menghapus data ini? (ya/tidak): ').strip().casefold()
        if yakin in ('ya', 'tidak'):
            break
        print("Masukkan 'ya' atau 'tidak'.")

    if yakin == 'tidak':
        print('Penghapusan dibatalkan.')
        pindah_menu()
        return

    #hapus satu baris saja lalu langsung simpan ke csv
    data = data.drop(index=data.index[posisi])
    data.to_csv(file, index=False)
    print('Status berhasil dikonfirmasi dan data berhasil dihapus.')
    pindah_menu()

def lihat_barang():
    bersihkan_layar()
    list_size = ceil(list_barang.shape[0] / 10)
    page = list_barang.loc[1:10, ['ID', 'kategori', 'keyword']]
    print(f"""Masukkan input berupa: 
    1. Nomor halaman 1 - {list_size}
    2. ID (untuk melihat detail barang)
    3. 0 (untuk kembali ke menu utama)""")
    while True:
        nomor_hal = input("> ")
        bersihkan_layar()
        if nomor_hal == '0':
            break
        elif len(nomor_hal) == 6:
            selected = list_barang.query('ID == @nomor_hal')
            if selected.empty:
                print("Tidak ada pengaduan dengan ID tersebut! Mohon input ulang")
                continue 
            detail_barang(selected.iloc[0], "pelaporan")
        elif (int(nomor_hal) > 0 and int(nomor_hal) <= list_size):
            nomor_hal = int(nomor_hal)
            page = list_barang.loc[1*(10*(nomor_hal-1)):10*(nomor_hal), ['ID', 'kategori', 'keyword']]
            print("="*17 + " List Barang Temuan " + "="*17)
            print(page)
            print(f"Halaman {nomor_hal} dari {list_size}")
        else:
            print("Opsi tidak tersedia! Tolong input ulang")

def lihat_aduan():
    bersihkan_layar()
    list_size = ceil(list_aduan.shape[0] / 10)
    page = list_aduan.loc[1:10, ['ID', 'kategori', 'keyword']]
    print(f"""Masukkan input berupa: 
    1. Nomor halaman 1 - {list_size}
    2. ID (untuk melihat detail barang)
    3. 0 (untuk kembali ke menu utama)""")
    while True:
        nomor_hal = input("> ")
        bersihkan_layar()
        if nomor_hal == '0':
            break
        elif len(nomor_hal) == 6:
            selected = list_aduan.query('ID == @nomor_hal')
            if selected.empty:
                print("Tidak ada pengaduan dengan ID tersebut! Mohon input ulang")
                continue 
            detail_barang(selected.iloc[0], "pengaduan")
        elif (int(nomor_hal) > 0 and int(nomor_hal) <= list_size):
            nomor_hal = int(nomor_hal)
            page = list_aduan.loc[1*(10*(nomor_hal-1)):10*(nomor_hal), ['ID', 'kategori', 'keyword']]
            print("="*17 + " List Barang Hilang " + "="*17)
            print(page)
            print(f"Halaman {nomor_hal} dari {list_size}")
        else:
            print("Opsi tidak tersedia! Tolong input ulang")

typing_effect("Selamat Datang di TemuIn!")
nama_lengkap = input("Masukkan Nama Lengkap Anda: ")
nim = input("Masukkan NIM Anda: ")
kontak = input("Masukkan Nomor Kontak Anda: ")
opsi = 0
while True:
    typing_effect("""Main Menu: Pilih Opsi yang Tersedia! (1-6)
        1. Melaporkan barang temuan
        2. Mencari barang hilang
        3. Mengadukan barang hilang
        4. Melihat list barang hilang
        5. Melihat list aduan barang dicari
        6. Konfirmasi status barang
        7. Exit""")
    opsi = input(">> ")
    if (opsi == "1"):
        pelaporan_barang(nama_lengkap,nim,kontak)
    elif (opsi == "2"):
        pencarian_barang()
    elif (opsi == "3"):
        pengaduan_barang(nama_lengkap,nim,kontak)
    elif (opsi == "4"):
        lihat_barang()
    elif (opsi == "5"):
        lihat_aduan()
    elif (opsi == "6"):
        konfirmasi_status()
    elif (opsi == "7"):
        typing_effect("Program telah berhenti. Terimakasih telah menggunakan TemuIn!")
        break
    else:
        typing_effect("Tolong pilih opsi yang sesuai!")
        continue

if (len(data_pengaduan) != 0):
    dict_pengaduan = {
        "nama_lengkap": [],
        "nim": [],
        "kontak": [],
        "ID": [],
        "kategori": [],
        "keyword": [],
        "deskripsi": [],
        "waktu": [],
        "lokasi": []
    }
    for row in data_pengaduan:
        i = 0
        for key in dict_pengaduan.keys():
            dict_pengaduan[key].append(row[i])
            i += 1
    df_pengaduan = pd.DataFrame(dict_pengaduan)
    list_aduan = pd.concat([list_aduan, df_pengaduan], axis=0)
    list_aduan.to_csv('pengaduan.csv', index=False)

if (len(data_pelaporan) != 0):
    dict_pelaporan = {
        "nama_lengkap": [],
        "nim": [],
        "kontak": [],
        "ID": [],
        "kategori": [],
        "keyword": [],
        "deskripsi": [],
        "waktu": [],
        "loc_found": [],
        "loc_pick": []
    }
    for row in data_pelaporan:
        i = 0
        for key in dict_pelaporan.keys():
            dict_pelaporan[key].append(row[i])
            i += 1
    df_pelaporan = pd.DataFrame(dict_pelaporan)
    list_barang = pd.concat([list_barang, df_pelaporan], axis=0)
    list_barang.to_csv('pelaporan.csv', index=False) 
# data pengaduan diubah menjadi dataframe sebelum digabung ke list_barang






# Dataframe list_barang dan list_aduan kita overwrite ke file database pada akhir program


# data_pencarian.append([a, b, c, ...])

# hasil filter sesuai input kategori dan input untuk pencarian barang hilang
# hasil_cari = list_barang.query(kategori == and keyword == )


# pakai try except buat cari data di df!
# df[header_name] untuk  akses kolom
# df.query(kategori == "-" and warna == "-", inplace=True) 
# df.empty() return true if empty

# delete row in DataFrame
# df.drop()