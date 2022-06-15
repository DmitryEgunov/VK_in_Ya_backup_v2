import requests
import time


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
                }

    def add_folder(self, folder_name):
        # Добавляем папку в корневой каталог Яндекс.Диск
        put_folder_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {"path": folder_name}
        response = requests.put(put_folder_url, headers=headers, params=params)
        return response

    def get_upload_link(self, yadisk_file_path: str, folder_name):
        # Получаем ссылку на размещение файла в папке на Яндекс.Диск
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": folder_name + "/" + yadisk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload(self, url_and_json, folder_name):
        # Загружаем фотографии максимального разрешения на
        # Яндекс.Диск по средствам ссылок из VK
        i = 0
        while i < int(len(url_and_json[1])):
            print(
            f"Запись фотографии {url_and_json[1][i]['file_name']} на Яндекс.Диск ({i + 1}/{int(len(url_and_json[1]))})")
            href = f"disk:/{folder_name}/{url_and_json[0][i]['file_name']}"
            url = url_and_json[0][i]['url']
            headers = self.get_headers()
            params = {"path": href, "url": url, "overwrite": "true"}
            response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload', params=params,
                                     headers=headers)
            response.raise_for_status()
            if response.status_code == 202:
                print('Success')
            time.sleep(0.33)
            i += 1
        print('Запись файла с данными о фотографиях на Яндекс.Диск')
        href_json = self.get_upload_link(yadisk_file_path='photo.json', folder_name=folder_name)
        href = href_json['href']
        response = requests.put(href, data=open('photo.json', 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('Success')

    def ya_main(self, vk_res):
        ya_token = input('Введите токен с полигона Яндекс.Диска: ')
        folder_name = input('Введите название папки для хранения файлов: ')

        url_and_json = vk_res

        Ya_uploader = YaUploader(token=ya_token)
        Ya_uploader.add_folder(folder_name)
        Ya_uploader.upload(url_and_json, folder_name)