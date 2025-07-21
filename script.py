import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# --- KONFIGURASI ---
START_URL = "https://id.mtlnovels.com/everlasting-dragon-emperor/chapter-1-rebirth/"
SAVE_FOLDER = "Novel - Everlasting Dragon Emperor"
MIN_DELAY = 1
MAX_DELAY = 5

# Buat folder penyimpanan jika belum ada
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# Inisialisasi WebDriver di luar blok try
# Ganti dengan webdriver.Chrome() atau browser lain jika perlu
driver = webdriver.Edge()

# =================================================================
# BLOK TRY...FINALLY PALING LUAR
# Tujuannya: Memastikan driver.quit() SELALU dijalankan di akhir.
# =================================================================
try:
    driver.get(START_URL)
    chapter_counter = 1

    # Loop utama untuk scraping, sekarang berada di dalam try utama
    while True:
        # =================================================================
        # BLOK TRY...EXCEPT DI DALAM LOOP
        # Tujuannya: Menangani error spesifik per bab (mis. bab terakhir)
        # =================================================================
        try:
            print("--------------------------------------------------")
            wait = WebDriverWait(driver, 30)

            # Ganti locator ini sesuai dengan investigasi Anda di situs target
            # Untuk id.mtlnovels.com, konten utama ada di dalam div dengan class 'entry-content'
            content_area = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "single-page")))

            print(f"Memproses Bab ke-{chapter_counter}...")

            # 1. Ambil Judul (Ganti locator jika perlu)
            title_element = driver.find_element(By.CLASS_NAME, "main-title")
            title_text = title_element.text
            safe_title = "".join(c for c in title_text if c.isalnum() or c in (' ', '-', '_')).rstrip()

            # 2. Ambil semua paragraf konten
            paragraphs = content_area.find_elements(By.TAG_NAME, "p")
            content_text = "\n".join([p.text for p in paragraphs])

            # 3. Siapkan nama file dan simpan
            file_name = f"{str(chapter_counter).zfill(3)} - {safe_title}.txt"
            file_path = os.path.join(SAVE_FOLDER, file_name)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"Judul: {title_text}\n\n")
                f.write(content_text)
            print(f"Berhasil disimpan sebagai: {file_name}")

            # 4. Cari dan klik tombol "Next Chapter"
            print("Mencari tombol 'Next Chapter'...")
            # Cari elemen <a> DENGAN class 'next' (ditulis 'a.next')
            next_button = driver.find_element(By.CSS_SELECTOR, "a.next")

            # Klik tombol tersebut
            driver.execute_script("arguments[0].click();", next_button)

            chapter_counter += 1

            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            print(f"Berpindah ke bab selanjutnya... Jeda selama {delay:.2f} detik.")
            time.sleep(delay)

        except (NoSuchElementException, TimeoutException):
            print("\n==================================================")
            print("Tombol 'Next Chapter' tidak ditemukan atau halaman timeout.")
            print("Proses scraping dianggap selesai.")
            print("==================================================")
            break  # Keluar dari loop while, lalu akan menuju ke blok finally utama.

        except Exception as e:
            print(f"Terjadi kesalahan tak terduga di dalam loop: {e}")
            break  # Keluar dari loop jika ada error lain

finally:
    print("Menutup browser...")
    driver.quit()

