from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os
from tqdm import tqdm


# Функция для создания директории, если она не существует
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# Функция для загрузки изображения по URL
def download_image(url, folder_path):
    # Создаем папку, если она не существует
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Получаем имя файла из URL
    filename = os.path.join(folder_path, url.split("/")[-1])

    # Запрос к URL для загрузки данных
    response = requests.get(url)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Записываем содержимое ответа в файл
        with open(filename, 'wb') as f:
            f.write(response.content)
        #print("Изображение успешно скачано и сохранено в", filename)
    else:
        print("Не удалось скачать изображение. Код ответа:", response.status_code)


# Функция для скачивания изображений с сайта
def download_images(url, folder_id, limit):
    # Создание директории для сохранения изображений
    create_directory(folder_id)

    # Счетчик скачанных изображений
    count = 0

    # Инициализация веб-драйвера
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.headless = False  # Отображение браузера (True - скрытый режим)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Открываем страницу
        driver.get(url)

        # Пауза для загрузки контента
        time.sleep(5)

        # Цикл прокрутки страницы до тех пор, пока не будет скачано достаточное количество изображений
        pbar = tqdm(total=limit, desc=f'Скачивание для папки {folder_id}')
        while count < limit:
            # Прокручиваем страницу вниз
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Пауза для загрузки контента

            # Получаем HTML-код страницы
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            # Поиск всех элементов с классом "item__img"
            img_divs = soup.find_all('div', class_='item__img')

            # Перебор найденных элементов
            for img_div in img_divs:
                # Получение тега <img>
                img_tag = img_div.find('img')

                if img_tag:
                    # Получение URL изображения из атрибута src
                    img_url = 'https://goskatalog.ru' + img_tag.get('src')
                    print(img_url)
                    if img_url:
                        # Загрузка изображения
                        download_image(img_url, str(folder_id))
                        # Увеличиваем счетчик скачанных изображений
                        count += 1
                        pbar.update(1)
                        if count >= limit:
                            break

        pbar.close()
        print(f"Скачивание для папки {folder_id} завершено.")
    finally:
        # Закрываем браузер после завершения работы
        driver.quit()


# URL сайтов и количество изображений для скачивания
sites = []

for i in range(1,16):
    str = f"https://goskatalog.ru/portal/#/collections?typologyId={i}"
    sites.append({"url": str, "folder_id": f"{i}", "limit": 5000})



# Скачивание изображений для каждого сайта
for site in sites:
    download_images(site['url'], site['folder_id'], site['limit'])