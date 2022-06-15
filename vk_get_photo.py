import requests
import configparser


class VK_users:
    config = configparser.ConfigParser()
    config.read('settings.ini')
    vk_token = ''.join(value.strip('"') for value in config['VK']['token'])
    url = 'https://api.vk.com/method/'
    def __init__(self, version):
        self.params = {'access_token': self.vk_token,
                       'v': version}

    def get_photos(self, user_input, num_of_fotos: int):
        # Определяем id пользователя (для случая ввода screen_name)
        url_get_users = self.url + 'users.get'
        ids_params = {'user_ids': user_input}
        res_ids = requests.get(url_get_users, params={**self.params, **ids_params}).json()
        user_id = res_ids['response'][0]['id']
        # Получаем json файл с данными по фотографиям пользователя
        url_get_photos = self.url + 'photos.get'
        get_params = {'extended': '1', 'owner_id': user_id, 'album_id': 'profile', 'count': int(num_of_fotos)}
        res = requests.get(url_get_photos, params={**self.params, **get_params}).json()
        res = res['response']['items']
        if num_of_fotos > len(res):
            num_of_fotos = len(res)
            print(f'У пользователя всего : {num_of_fotos} фотографий.')
        return res

    def get_max_size(self, res):
        # Ищем максимальное расширение фотографий в json файле
        i = 0
        max_list1 = []
        while i < len(res):
            max_dict = {}
            lname = str(res[i]['likes']['count'])
            dname = str(res[i]['date'])
            for photo in res[i]['sizes']:
                type = photo['type']
                url = photo['url']
                max_dict.update({photo['height'] * photo['width']: [{'lname': lname},\
                                {'dname': dname}, {'type': type}, {'url': url}]})
                best_photo = max(max_dict.items(), key=lambda x: x[0])
            i += 1
            max_list1.append(best_photo)
        return max_list1

    def json_photos_file(self, max_list):
        temp = []
        json_file = []
        url_to_download = []
        i = 0
        while i < len(max_list):
            lname = str(max_list[i][1][0]['lname'])
            dname = str(max_list[i][1][1]['dname'])
            size = max_list[i][1][2]['type']
            url = max_list[i][1][3]['url']
            if str(lname + '.jpg') not in temp:
                temp1 = {'file_name': str(lname) + '.jpg', 'size': size}
                temp2 = {'file_name': str(lname) + '.jpg', 'url': url}
                temp.append(str(lname + '.jpg'))
                json_file.append(temp1)
                url_to_download.append(temp2)
            elif str(lname + '.jpg') in temp:
                temp1 = {'file_name': str(lname) + str(dname) + '.jpg', 'size': size}
                temp2 = {'file_name': str(lname) + str(dname) + '.jpg', 'url': url}
                temp.append(str(lname + dname + '.jpg'))
                json_file.append(temp1)
                url_to_download.append(temp2)
            i += 1
        return (url_to_download, json_file)

    def vk_main(self):
        id_vk_user = input('Введите id пользователя VK или его ник: ')
        num_of_fotos_vk_user = int(input('Введите количество загружаемых фотографий: '))

        VK_user = VK_users('5.131')
        max_list = VK_user.get_max_size(VK_user.get_photos(id_vk_user, num_of_fotos_vk_user))
        vk_res = VK_user.json_photos_file(max_list)
        return vk_res
