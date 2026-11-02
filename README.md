# TemuIn

Sistem pencarian dan pelaporan barang hilang

## Description

Repository ini dibuat dalam rangka memenuhi Tugas Besar mata kuliah Berpikir Komputasional. Secara umum, TemuIn berusaha menyelesaikan masalah mahasiswa ITB, yaitu belum adanya sistem pelaporan barang hilang yang terintegrasi langsung dengan penitipan barang hilang. Program ini dibangun menggunakan perulangan while, fungsi (def), percabangan (if-else), serta mengimpor beberapa modul seperti os, sys, csv, shutil, uuid, pandas, hingga prompt_toolkit. Adapun fitur-fitur program ini diantaranya:
1. Pelaporan barang temuan, termasuk menyimpan datanya
2. Pencarian barang hilang di database
3. Pengaduan barang hilang, termasuk menyimpan datanya
4. Melihat daftar barang temuan yang sudah masuk di database
5. Melihat daftar aduan yang sudah masuk di database
6. Mengonfirmasi status pengembalian barang, termasuk menghapus datanya dari database

## Getting Started

### Dependencies & Installing

Untuk menjalankan program ini, Anda dapat mengunduh folder source_code yang berisi folder penyimpanan gambar, kode utama, serta penyimpan data dalam bentuk csv. Jangan lupa untuk ekstrak zip gambarnya!

Program ini memakai 2 modul diluar bawaan python, yaitu pandas dan prompt_toolkit. Oleh karena itu, Anda perlu menjalankan kode berikut di terminal sebelum dapat menggunakan program:

```bash
pip install pandas prompt-toolkit
```

## Authors

Program ini disusun oleh kelompok 9 Berpikir Komputasional K36, dengan anggota:
1. Gilbert Maxwell (19626016)
2. Fernando Almer Renjiro (19626076)
3. Rasya Syamil Mumtaz (19626166)
4. Ali Fahriza Ahda Yusroni (19626202)
