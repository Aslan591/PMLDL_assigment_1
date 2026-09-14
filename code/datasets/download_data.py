import os
import urllib.request

RAW_DATA_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
RAW_DATA_PATH = os.path.join("data", "raw", "titanic.csv")

def download_data():
    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
    if os.path.exists(RAW_DATA_PATH):
        print(f"Файл уже существует: {RAW_DATA_PATH}")
        return
    print(f"Скачиваю данные из {RAW_DATA_URL}...")
    urllib.request.urlretrieve(RAW_DATA_URL, RAW_DATA_PATH)
    print(f"Сохранено в {RAW_DATA_PATH}")

if __name__ == "__main__":
    download_data()