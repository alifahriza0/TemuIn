'''
Author              : Kelompok 9
Tanggal Pengerjaan  : 19 Oktober - 1 November 2026

PROGRAM TemuIn - PENCARIAN DAN PELAPORAN BARANG HILANG
Deskripsi           : Simulasi sistem Lost And Found lingkungan ITB dengan fitur-fitur berupa pelaporan barang temuan, pencarian dan pengaduan
                      barang hilang, melihat list barang dan aduan, serta konfirmasi barang telah dikembalikan.

KAMUS
nama_lengkap            = variabel penyimpan nama lengkap pengguna
nim                     = variabel penyimpan NIM pengguna
kontak                  = variabel penyimpan kontak pengguna
opsi                    = variabel penyimpan pilihan alur pengguna
kategori_temuan         = variabel penyimpan kategori barang temuan
id_temuan               = variabel penyimpan ID barang temuan
keyword_temuan          = variabel penyimpan kata kunci barang temuan
deskripsi_temuan        = variabel penyimpan deskripsi singkat detail barang temuan
waktu_temuan            = variabel penyimpan waktu barang ditemukan sesuai format
lokasi_temuan           = variabel penyimpan lokasi barang ditemukan
foto_temuan             = variabel penyimpan nama file foto barang temuan setelah format disesuaikan
lokasi_pengambilan      = variabel penyimpan lokasi penitipan barang temuan
kategori_aduan          = variabel penyimpan kategori aduan barang hilang
id_aduan                = variabel penyimpan ID aduan barang hilang
keyword_aduan           = variabel penyimpan kata kunci aduan barang hilang
deskripsi_aduan         = variabel penyimpan deskripsi singkat detail aduan barang hilang
waktu_aduan             = variabel penyimpan waktu barang hilang sesuai format
lokasi_aduan            = variabel penyimpan lokasi barang hilang
foto_aduan              = variabel penyimpan nama file foto barang yang hilang setelah format disesuaikan
data_pelaporan          = list penyimpan data pelaporan sebelum dimasukkan ke csv
data_pengaduan          = list penyimpan data pengaduan sebelum dimasukkan ke csv
list_barang             = data frame penyimpan dan pembaca data seluruh laporan barang temuan
list_aduan              = data frame penyimpan dan pembaca data seluruh aduan barang hilang
typing_effect           = fungsi efek print di terminal
bersihkan_layar         = fungsi mengosongkan tampilan terminal
pindah_menu             = fungsi pindah ke menu lain
pilih_autofill          = fungsi menampilkan opsi dengan word completer
generate_id             = fungsi membuat id acak untuk penyimpanan foto dan data
simpan_csv              = fungsi menyimpan data pelaporan atau pengaduan ke pelaporan.csv atau pengaduan.csv
detail_barang           = fungsi menampilkan rincian barang temuan atau barang hilang
input_waktu             = fungsi menerima waktu barang ditemukan/hilang dengan format tertentu
input_gambar            = fungsi menerima input file gambar, mengubah nama file sesuai format, dan menyalin ke folder yang sesuai
pelaporan_barang        = fungsi melaporkan barang temuan lalu disimpan ke database
pencarian_barang        = fungsi mencari barang di database yang sesuai dengan kategori dan keyword input
pengaduan_barang        = fungsi mengadukan barang hilang lalu disimpan ke database
lihat_barang            = fungsi menampilkan daftar barang temuan yang ada di database
lihat_aduan             = fungsi menampilkan daftar aduan barang hilang yang ada di database
konfirmasi_status       = fungsi konfirmasi status barang temuan atau aduan untuk dihilangkan dari database
kategori                = list kategori barang yang dicari atau dilaporkan sebagai wordcompleter
loc_ambil               = list lokasi penitipan barang temuan yang dilaporkan sebagai wordcompleter
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

#Opsi kategori dan lokasi penitipan barang untuk Word Completer
kategori = ['Elektronik', 'ATK', 'Dompet', 'Kartu', 'Pakaian & Aksesoris', 'Kunci', 'Alat Ibadah', 'Wadah Konsumsi']
loc_ambil = ['GKU 1', 'GKU 2', 'GKU 3', 'Gedung A/E', 'Gedung Utama', 'Sekretariat Ditsama']

#Deklarasi variabel global
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
        typing_effect("Pilihan tidak tersedia. Silakan pilih dari daftar yang disediakan.")

def generate_id(list_data, mode):
    prefix = ""
    # Menentukan karakter pertama sesuai mode
    # L untuk laporan dan A untuk aduan
    if (mode == "Pelaporan"):
        prefix = 'L'
    else:
        prefix = 'A'

    # ID didapatkan dari penggunaan modul uuid. Sistem memotong menjadi 5 karakter dari modul uuid
    # Prefix digabung dengan potongan string dari modul
    id = (prefix + str(uuid.uuid1())[0:5]).upper()
    # Melakukan pengulangan jika ID sudah ada di file database
    while ((list_data['ID'] == id).any()):
        id = (prefix + str(uuid.uuid1())[0:5]).upper()

    return id

def simpan_csv():
    global list_barang, list_aduan, data_pelaporan, data_pengaduan
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
            "lokasi": [],
            "path_gambar": []
        }
        # iterasi tiap baris dari data pengaduan
        for row in data_pengaduan:
            i = 0
            # iterasi tiap kunci di dictionary dict_pengaduan
            for key in dict_pengaduan.keys():
                # tambahkan value baris ke-i untuk tiap key ke-i 
                # (key dan nilai dari list baris data_pengaduan sengaja dibentuk urutan yang sama)
                dict_pengaduan[key].append(row[i])
                i += 1
        # dict_pengaduan diubah menjadi bentuk dataframe
        df_pengaduan = pd.DataFrame(dict_pengaduan)
        # bentuk dataframe-nya kita gabung dengan dataframe utama (list_aduan)
        list_aduan = pd.concat([list_aduan, df_pengaduan], axis=0, ignore_index=True)
        list_aduan.index += 1
        # overwrite ke pengaduan.csv untuk menyimpan data 
        list_aduan.to_csv('pengaduan.csv', index=False)
        data_pengaduan.clear()

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
            "loc_pick": [],
            "path_gambar": []
        }
        #iterasi baris dari list data_pelaporan
        for row in data_pelaporan:
            i = 0
            # iterasi key dari dict_pelaporan
            for key in dict_pelaporan.keys():
                # tambahkan value baris ke-i untuk tiap key ke-i 
                # (key dan nilai dari list baris data_pengaduan sengaja dibentuk urutan yang sama)  
                dict_pelaporan[key].append(row[i])
                i += 1
        # ubah bentuk dictionary menjadi dataframe
        df_pelaporan = pd.DataFrame(dict_pelaporan)
        # gabung dataframe di atas dengan dataframe utama
        list_barang = pd.concat([list_barang, df_pelaporan], axis=0, ignore_index=True)
        list_barang.index += 1
        list_barang.to_csv('pelaporan.csv', index=False) 
        data_pelaporan.clear()

def detail_barang(barang, mode):
    #menampilkan detail dari barang yang dipilih
    pindah_menu()
    typing_effect('=== DETAIL BARANG ===')

    print(f"ID                  : {barang['ID']}")
    print(f"Nama barang         : {barang['keyword']}")
    print(f"Kategori            : {barang['kategori']}")
    print(f"Deskripsi           : {barang['deskripsi']}")
    print(f"Waktu ditemukan     : {barang['waktu']}")
    #Menentukan folder tempat disimpannya gambar berdasarkan mode 
    if mode == "pelaporan":
        print(f"Lokasi ditemukan    : {barang['loc_found']}")
        folder_tujuan = "gambar_pelaporan"
    else:
        print(f"Lokasi hilang       : {barang['lokasi']}")
        folder_tujuan = "gambar_pengaduan"
    #Membuat path foto untuk dibuka
    file_foto = os.path.join(folder_tujuan, barang['path_gambar'])
    #Membuka file foto sesuai path di data path_gambar
    os.startfile(file_foto)

def input_waktu(pesan):
    #Menginisiasi format waktu input
    format = "%d/%m/%y %H.%M"
    while True:
        waktu_user = input(pesan).strip()
        #Memastikan input waktu sesuai format
        try:
            waktu_valid = datetime.strptime(waktu_user, format)
            return waktu_valid.strftime(format)
        except ValueError:
            typing_effect("Format salah! Pastikan menggunakan format 'dd/mm/yy HH.MM'!")

def input_gambar(id, csv_path, folder_tujuan):
    #Membuat folder kumpulan gambar jika belum ada
    os.makedirs(folder_tujuan, exist_ok=True)
    while True:
        #Menerima path file foto di komputer
        foto = input("Drag and Drop gambar Anda dan klik Enter!").strip()
        #Menghapus &, \, ' jika ada, sehingga hanya diambil nama filenya
        if foto.startswith("& "):
            foto = foto [1:].strip()
        foto = foto.strip('\'" ')
        #Mengecek jika file foto ada di komputer pengguna
        if foto and os.path.exists(foto):
            break
        else:
            typing_effect("Gambar tidak valid, silahkan input ulang.")
    #Mengakses csv pelaporan/pengaduan di baris terakhir
    jumlah_baris = 0
    with open(csv_path, mode='r', encoding='utf-8') as f:
        for line in f:
            jumlah_baris += 1
    #Mengambil ekstensi foto dan membuat nama foto
    ekstensi = os.path.splitext(foto)[1]
    nama_csv = csv_path.split(".")[0]
    nama_foto = f"foto_{nama_csv}_{id}{ekstensi}"
    #Menyalin foto di folder tujuan
    foto_temuan = os.path.join(folder_tujuan, nama_foto)
    shutil.copy(foto, foto_temuan)
    return nama_foto

def pelaporan_barang(nama_lengkap, nim, kontak):
    pindah_menu()
    typing_effect("=== PELAPORAN BARANG TEMUAN ===")
    #Menerima input rincian barang hilang serta membuat id acak
    kategori_temuan = pilih_autofill("Apa kategori barang yang Anda temukan? ", kategori)
    typing_effect("Berikan keyword dari barang yang Anda temukan.\nPetunjuk : Gunakan Format 'Jenis Barang' + 'Merk atau warna'\nContoh : 'Laptop Lenovo', 'Jaket Hitam'")
    id_temuan = generate_id(list_barang, "Pelaporan")
    keyword_temuan = input("Masukkan keyword: ")
    deskripsi_temuan = input("Berikan deskripsi dari barang yang Anda temukan: ")
    waktu_temuan = input_waktu("Masukkan waktu barang ditemukan (dd/mm/yy HH.MM): ")
    lokasi_temuan = input("Dimana barang ini ditemukan? ")
    foto_temuan = input_gambar(id_temuan, "pelaporan.csv","gambar_pelaporan")   
    lokasi_pengambilan = pilih_autofill("Pilih salah satu lokasi berikut untuk menitipkan barang: ", loc_ambil)
    #Menggabungkan detail detail barang dalam data_pelaporan
    data_pelaporan.append([nama_lengkap, nim, kontak, id_temuan,kategori_temuan, keyword_temuan, 
                           deskripsi_temuan, waktu_temuan, lokasi_temuan, lokasi_pengambilan, foto_temuan])
    #Menyimpan data_pelaporan di csv
    simpan_csv()
    typing_effect(f"Laporan sudah masuk di {datetime.now()}!")
    time.sleep(1)
    typing_effect("Terima kasih atas laporannya! Semoga bermanfaat ya :)")
    pindah_menu()

def pencarian_barang(nama_lengkap,nim,kontak):
    pindah_menu()
    typing_effect('=== PENCARIAN BARANG HILANG ===')
    
    data = pd.read_csv('pelaporan.csv', dtype=str).fillna('') #ubah nilai kosong dengan string "" agar saat casefold tidak error
    #Jika data pelaporan masih kosong, user akan dialihkan ke menu utama
    if data.empty:
        typing_effect('Belum ada barang yang dilaporkan.')
        pindah_menu()
        return

    kategori_dicari = pilih_autofill('Kategori barang yang dicari: ', kategori)
    #Mengambil kolom kategori, dicocokkan dengan kategori yang dicari, menghasilkan True/False --> diambil true
    hasil_kategori = data[data['kategori'].str.casefold() == kategori_dicari.casefold()] #Mengubah kategori input jadi huruf kecil

    if hasil_kategori.empty:
        typing_effect('Belum ada barang dengan kategori tersebut.')
        pindah_menu()
        return #menghentikan fungsi pencarian barang

    #Mencari semua kemungkinan keyword yang sesuai dengan kategori
    daftar_keyword = list(hasil_kategori['keyword'].drop_duplicates())
    saran = WordCompleter(daftar_keyword, ignore_case=True, sentence=True) #Melihat kalimat keyword secara keseluruhan
    #Mengulang pencarian keyword kalau pengguna ingin mencoba lagi
    while True:
        keyword = prompt('Kata kunci barang: ', completer=saran).strip()
        if keyword == '':
            typing_effect('Kata kunci tidak boleh kosong.')
            continue
        
        #Mencari barang dengan keyword itu di database
        hasil = hasil_kategori[hasil_kategori['keyword'].str.contains(keyword, case=False, regex=False)]
        if hasil.empty:
            typing_effect('Barang belum ditemukan.')
            ulang = input('Cari keyword lain? (ya/tidak): ').strip().casefold()
            if ulang == 'ya':
                continue
            else: 
                pindah_menu()
                return

        #Mengulang tampilan hasil kalau mau memilih barang lain
        while True:
            print('\n=== HASIL PENCARIAN ===')
            #_ mengartikan index di hasil itu tidak dipakai. iterrows=mengiterasi rows
            for _, data_barang in hasil.iterrows():
                print(f"ID: {data_barang['ID']} | {data_barang['keyword']} | {data_barang['deskripsi']}")
            while True:
                id_dipilih = input('Masukkan ID barang (0 untuk kembali): ').strip()
                if id_dipilih == '0':
                    pindah_menu()
                    return
                #Mencari baris di csv yang dengan ID yang sama dengan input pengguna
                else:
                    barang_cocok = hasil[hasil['ID'].str.casefold() == id_dipilih.casefold()]
                if not barang_cocok.empty:
                    break
                else:
                    typing_effect('ID barang tidak tersedia.')

            #Mengambil satu baris barang berdasarkan ID, menampilkan detail barang yang dipilih
            barang = barang_cocok.iloc[0]
            detail_barang(barang, "pelaporan")
            #Menanyakan kesesuaian barang, memastikan jawabannya hanya ya atau tidak
            while True:
                yakin = input('Apakah ini barang yang Anda cari? (ya/tidak): ').strip().casefold()
                if yakin in ['ya', 'tidak']:
                    break
                else:
                    print("Masukkan 'ya' atau 'tidak'.")
            #Jika jawabannya ya, menampilkan lokasi pengambilan, identitas pelapor, serta instruksi konfirmasi
            if yakin == 'ya':
                typing_effect('\nBarang yang Anda cari mungkin sudah ditemukan.')
                typing_effect(f"Silakan datang ke {barang['loc_pick']} dan membawa KTM.")
                typing_effect('Petugas akan memeriksa kepemilikan barang.')
                typing_effect(f"Silahkan hubungi {barang['nama_lengkap']} dengan kontak {barang['kontak']} jika ada yang ingin ditanyakan")
                typing_effect('Setelah pengambilan, mintalah informasi NIM pelapor kepada petugas')
                typing_effect('untuk konfirmasi status pada opsi menu 6.')
                time.sleep(5)
                pindah_menu()
                return
            
            #Jika jawabannya tidak, user boleh pilih langkah berikutnya
            typing_effect('\nBarang ini bukan yang Anda cari.')
            typing_effect('1. Lihat barang lainnya dalam kategori yang sama')
            typing_effect('2. Cari kategori lain')
            typing_effect('3. Buat pengaduan barang hilang')
            typing_effect('0. Kembali ke menu utama')

            #Memroses program sesuai pilihan opsi user
            while True:
                lanjut = int(input('Pilih opsi: '))
                if lanjut in [0, 1, 2, 3]:
                    break
                print('Pilihan tidak tersedia.')
            if lanjut == 0:
                pindah_menu()
                return
            if lanjut == 1:
                pindah_menu()
                continue
            if lanjut == 2:
                pindah_menu()
                break
            if lanjut == 3:
                pengaduan_barang(nama_lengkap, nim, kontak)
                return


def pengaduan_barang(nama_lengkap, nim, kontak):
    pindah_menu()
    typing_effect("=== PENGADUAN BARANG HILANG ===")
    #Menerima input detail barang dan membuat id acak
    kategori_aduan = pilih_autofill("Apa kategori barang Anda yang hilang? ", kategori)
    typing_effect("Berikan keyword dari barang yang Anda ingin adukan.\nPetunjuk : Gunakan Format 'Jenis Barang' + 'Merk atau warna'\nContoh : 'Laptop Lenovo', 'Jaket Hitam'")
    id_aduan = generate_id(list_aduan, "Pengaduan")
    keyword_aduan = input("Masukkan keyword: ")
    deskripsi_aduan = input("Berikan deskripsi dari barang yang Anda adukan: ")
    waktu_aduan = input_waktu("Masukkan waktu barang diadukan (dd/mm/yy HH.MM): ")
    lokasi_aduan = input("Dimana barang ini hilang? ")
    foto_aduan = input_gambar(id_aduan, "pengaduan.csv", "gambar_pengaduan")
    #Menggabungkan detail barang ke data_pengaduan
    data_pengaduan.append([nama_lengkap, nim, kontak, id_aduan,kategori_aduan, keyword_aduan, 
                               deskripsi_aduan, waktu_aduan, lokasi_aduan, foto_aduan])
    #Menyimpan data_pengaduan di csv
    simpan_csv()
    typing_effect(f"Aduan sudah masuk di {datetime.now()}!")
    time.sleep(2)
    typing_effect("Terima kasih atas Aduannya! Semoga cepat ketemu ya :)")
    pindah_menu()

def lihat_barang(nama_lengkap,nim,kontak):
    bersihkan_layar()
    # Cek apabila data barang temuan kosong atau tidak
    if list_barang.empty:
        typing_effect("Belum ada barang yang dilaporkan.")
        pindah_menu()
        return
    # Menentukan ukuran dataframe untuk acuan jumlah halaman
    # 1 halaman 10 baris barang
    list_size = ceil(list_barang.shape[0] / 10)
    # Menyiapkan halaman pertama dari baris barang 1 - 10
    page = list_barang.iloc[0:10][['ID', 'kategori', 'keyword']]
    typing_effect(f"""Masukkan input berupa: 
    1. Nomor halaman 1 - {list_size}
    2. ID (untuk melihat detail barang)
    3. 0 (untuk kembali ke menu utama)""")
    while True:
        # melakukan uppercase pada input karena ID bersifat case-insensitive
        nomor_hal = input("> ").strip().upper()
        # Cek jika input pengguna bukan sebuah ID (yang memiliki 6 karakter kombinasi huruf dan angka)
        if len(nomor_hal) != 6: 
            try:
                # Mencoba mengubah input menjadi bentuk int
                int(nomor_hal)
            except:
                # Masuk blok kode ini apabila muncul error (TypeError karena input berupa char atau string)
                print("Input invalid! Mohon input ulang")
                continue
        bersihkan_layar()
        if nomor_hal == '0':
            break
        elif len(nomor_hal) == 6:
            # memilih baris dengan ID sesuai input pengguna
            selected = list_barang.query('ID == @nomor_hal')
            if selected.empty:
                typing_effect("Tidak ada laporan dengan ID tersebut! Mohon input ulang")
                continue
            #Menampilkan detail barang yang sesuai dengan ID yang dipilih
            barang = selected.iloc[0]
            detail_barang(barang, "pelaporan")
            while True:
                yakin = input('Apakah ini barang yang Anda cari? (ya/tidak): ').strip().casefold()
                if yakin in ['ya', 'tidak']:
                    break
                else:
                    print("Masukkan 'ya' atau 'tidak'.")
            if yakin == 'ya':
                typing_effect('\nBarang yang Anda cari mungkin sudah ditemukan.')
                typing_effect(f"Silakan datang ke {barang['loc_pick']} dan membawa KTM.")
                typing_effect('Petugas akan memeriksa kepemilikan barang.')
                typing_effect(f"Silahkan hubungi {barang['nama_lengkap']} dengan kontak {barang['kontak']} jika ada yang ingin ditanyakan")
                typing_effect('Setelah pengambilan, mintalah informasi NIM pelapor kepada petugas')
                typing_effect('untuk konfirmasi status pada opsi menu 6.')
                time.sleep(5)
                pindah_menu()
                return
            
            #Jika tidak yakin, user boleh pilih langkah berikutnya
            typing_effect('\nBarang ini bukan yang Anda cari.')
            typing_effect('1. Lihat barang lainnya')
            typing_effect('2. Buat aduan barang hilang')
            typing_effect('0. Kembali ke menu utama')

            while True:
                lanjut = int(input('Pilih opsi: '))
                if lanjut in [0, 1, 2]:
                    break
                print('Pilihan tidak tersedia.')
            if lanjut == 0:
                pindah_menu()
                return
            if lanjut == 1:
                bersihkan_layar()
                typing_effect(f"""Masukkan input berupa: 
        1. Nomor halaman 1 - {list_size}
        2. ID (untuk melihat detail barang)
        3. 0 (untuk kembali ke menu utama)""")
                continue
            if lanjut == 2:
                pengaduan_barang(nama_lengkap,nim,kontak)
                return
        elif (int(nomor_hal) > 0 and int(nomor_hal) <= list_size):
            nomor_hal = int(nomor_hal)
            # penentuan penampilan halaman dilakukan dengan kalkulasi berikut
            # semisal input nomor_hal = 2
            # 1 x (10 x (2-1)): 10 x 2 = 10:20 => menampilkan barang ke-10 hingga ke-20
            page = list_barang.iloc[1*(10*(nomor_hal-1)):10*(nomor_hal)][['ID', 'kategori', 'keyword']]
            print("="*17 + " List Barang Temuan " + "="*17)
            print(page)
            print(f"Halaman {nomor_hal} dari {list_size}")
        else:
            typing_effect("Opsi tidak tersedia! Tolong input ulang")
    pindah_menu()

def lihat_aduan():
    bersihkan_layar()
    if list_aduan.empty:
        typing_effect("Belum ada aduan.")
        pindah_menu()
        return
    # Mendapatkan ada berapa halaman yang bisa dibuat (1 halaman 10 barang)
    list_size = ceil(list_aduan.shape[0] / 10)
    # Mendapatkan dataframe berupa 10 baris aduan dengan tertera kolom ID, kategori, dan keyword
    page = list_aduan.iloc[1:10][['ID', 'kategori', 'keyword']]
    typing_effect(f"""Masukkan input berupa: 
    1. Nomor halaman 1 - {list_size}
    2. ID (untuk melihat detail barang)
    3. 0 (untuk kembali ke menu utama)""")
    while True:
        nomor_hal = input("> ").strip().upper()
        if len(nomor_hal) != 6: 
            try:
                # Cek apakah input berupa int atau bukan
                int(nomor_hal)
            except:
                # Masuk ke blok ini jika error (TypeError karena input bukan int)
                print("Input invalid! Mohon input ulang")
                continue
        bersihkan_layar()
        # Kembali ke menu utama
        if nomor_hal == '0':
            break
        # Jika input berupa 6 karakter, sistem menganggap user ingin memilih aduan dengan ID-nya
        elif len(nomor_hal) == 6:
            # Memilih aduan yang ID-nya sesuai
            selected = list_aduan.query('ID == @nomor_hal')
            if selected.empty:
                typing_effect("Tidak ada pengaduan dengan ID tersebut! Mohon input ulang")
                continue 
            barang = selected.iloc[0]
            detail_barang(barang, "pengaduan")
            while True:
                yakin = input('Apakah ini aduan yang Anda cari? (ya/tidak): ').strip().casefold()
                if yakin in ['ya', 'tidak']:
                    break
                else:
                    print("Masukkan 'ya' atau 'tidak'.")
            if yakin == 'ya':
                typing_effect(f"Silahkan hubungi {barang['nama_lengkap']} dengan kontak {barang['kontak']} untuk mengembalikan barang")
                typing_effect('Setelah pengembalian, mintalah informasi NIM pengadu')
                typing_effect('untuk konfirmasi status pada opsi menu 6.')
                time.sleep(3)
                pindah_menu()
                return
            
            #Jika tidak yakin, user boleh pilih langkah berikutnya
            typing_effect('\nAduan ini bukan yang Anda cari.')
            typing_effect('1. Lihat aduan lainnya')
            typing_effect('0. Kembali ke menu utama')

            while True:
                lanjut = int(input('Pilih opsi: '))
                if lanjut in [0, 1]:
                    break
                print('Pilihan tidak tersedia.')
            if lanjut == 0:
                pindah_menu()
                return
            if lanjut == 1:
                bersihkan_layar()
                typing_effect(f"""Masukkan input berupa: 
        1. Nomor halaman 1 - {list_size}
        2. ID (untuk melihat detail aduan)
        3. 0 (untuk kembali ke menu utama)""")
                continue
        # Jika input berada di rentang halaman yang ada
        elif (int(nomor_hal) > 0 and int(nomor_hal) <= list_size):
            nomor_hal = int(nomor_hal)
            page = list_aduan.iloc[1*(10*(nomor_hal-1)):10*(nomor_hal)][['ID', 'kategori', 'keyword']]
            print("="*17 + " List Barang Hilang " + "="*17)
            print(page)
            print(f"Halaman {nomor_hal} dari {list_size}")
        else:
            typing_effect("Opsi tidak tersedia! Tolong input ulang")
    pindah_menu()

def konfirmasi_status():
    pindah_menu()
    #Menentukan tipe data yang mau dikonfirmasi
    typing_effect('=== KONFIRMASI STATUS BARANG ATAU ADUAN ===')
    typing_effect('1. Konfirmasi pelaporan barang temuan')
    typing_effect('2. Konfirmasi pengaduan barang hilang')
    typing_effect('0. Kembali ke menu utama')
    while True:
        jenis= input('Pilih menu: ')
        try:
            jenis = int(jenis)
        except:
            print("Pilihan invalid!")
            continue

        if jenis in [0, 1, 2]:
            break
        print('Pilihan tidak tersedia')

    if jenis==0:
        pindah_menu()
        return
    #Membaca csv sesuai data yangdipilih
    file = 'pelaporan.csv' if jenis==1 else 'pengaduan.csv'
    data = pd.read_csv(file, dtype=str).fillna('')
    if data.empty:
        print('Belum ada data yang bisa dikonfirmasi.')
        pindah_menu()
        return
    #Menerima id barang atau aduan yang mau dikonfirmasi
    while True:
        id_dipilih = input('Masukkan ID data yang ingin dikonfirmasi (0 untuk kembali): ').strip()
        if id_dipilih=='0':
            pindah_menu()
            return
        #Mencari data dengan id yang sesuai
        data_cocok = data[data['ID'].str.casefold()==id_dipilih.casefold()]
        if not data_cocok.empty:
            break
        print('ID data tidak tersedia.')
    nim_asli= data_cocok.iloc[0]['nim'].strip()
    salah= True
    #Tiga kali kesempatan input nim, percobaan=0, 1, 2
    for percobaan in range(3):
        nim_input = input('Masukkan NIM pelapor/pengadu: ').strip()
        if nim_input==nim_asli:
            salah=False
            break
        else:
            sisa= 2-percobaan
        if sisa > 0:
            print(f'NIM tidak cocok. Kesempatan tersisa: {sisa}')
    #Jika kesempatan user habis, maka akan dialihkan ke menu utama
    if salah:
        typing_effect('Batas percobaan telah tercapai.')
        pindah_menu()
        return
    #Menampilkan detail barang yang dipilih
    while True:
        if jenis == 1:
            detail_barang(data_cocok.iloc[0], "pelaporan")
        else:
            detail_barang(data_cocok.iloc[0], "pengaduan")
        yakin = input('Apakah Anda yakin ingin menghapus data ini? (ya/tidak): ').strip().casefold()
        if yakin in ('ya', 'tidak'):
            break
        typing_effect("Masukkan 'ya' atau 'tidak'.")
    #Jika user tidak yakin, dialihkan ke menu utama
    if yakin == 'tidak':
        typing_effect('Penghapusan dibatalkan.')
        pindah_menu()
        return
    #jika user yakin, gambar dan path di csv akan dihapus
    else:
        #Menghapus gambar dari folder yang sesuai data
        folder_gambar = "gambar_pelaporan" if file == 'pelaporan.csv' else "gambar_pengaduan"
        path_hapus = os.path.join(folder_gambar, data_cocok.iloc[0]['path_gambar'])
        #Menghapus satu baris saja lalu langsung simpan ke csv
        os.remove(path_hapus)
        data= data.drop(data_cocok.index[0]) #ini masih menghapus 
        data.to_csv(file, index=False) #Menyimpan csv tanpa penambahan indeks
        typing_effect('Status berhasil dikonfirmasi dan data berhasil dihapus.')
        pindah_menu()

bersihkan_layar()
typing_effect("Selamat Datang di TemuIn!")
#Menerima input identitas pengguna
nama_lengkap = input("Masukkan Nama Lengkap Anda: ")
nim = input("Masukkan NIM Anda: ")
kontak = input("Masukkan Nomor Kontak Anda: ")
opsi = 0
while True:
    typing_effect("""Main Menu: Pilih Opsi yang Tersedia! (1-7)
        1. Melaporkan barang temuan
        2. Mencari barang hilang
        3. Mengadukan barang hilang
        4. Melihat list barang temuan
        5. Melihat list aduan barang dicari
        6. Konfirmasi status barang
        7. Exit""")
    opsi = input(">> ")
    #Memroses alur program berdasarkan opsi pilihan pengguna
    if (opsi == "1"):
        pelaporan_barang(nama_lengkap,nim,kontak)
    elif (opsi == "2"):
        pencarian_barang(nama_lengkap,nim,kontak)
    elif (opsi == "3"):
        pengaduan_barang(nama_lengkap,nim,kontak)
    elif (opsi == "4"):
        lihat_barang(nama_lengkap,nim,kontak)
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