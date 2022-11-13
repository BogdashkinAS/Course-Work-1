import time
import requests
import json
import sys
import urllib.parse
import datetime
import logging
from pprint import pprint
from progress.bar import ShadyBar

class YandexDisk:
        
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def get_files_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        pprint(response.json())
        return response.json()

    def upload_file_to_disk(self, disk_file_path, filename):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")

    def create_folder(self, path):
        folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        requests.put(f'{folder_url}?path={path}', headers=headers)

    def create_file_photo(self, folder, url):
        file_photo_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        url = urllib.parse.quote(url)
        requests.post(f'{file_photo_url}?path={folder}&url={url}', headers=headers)
        
class VK_USER:
    
    def vk_info(user_id):
        with open('token.txt', 'r') as file_object:
            token = file_object.read().strip()
            
        URL = 'https://api.vk.com/method/photos.get'
        params = {
            'user_id': user_id,
            'access_token': token,
            'v':'5.131',
            'album_id': 'profile',
            'extended': '1', 
            'photo_sizes': '1'
        }
        
        res = requests.get(URL, params=params).json()
        len_all_photo = len(res['response']['items'])
        all_photo = res['response']['items']
        height = 0
        width = 0
        url_max = ''
        photo_dict = []
        photo_dict_all = []
        file_name_list = []
        likes = 0
        file_name = ''
        size_type = ''
        size = ''
        date1 = ''
        date = ''
        iteration = 0

        if len(all_photo) > 5:
            iteration = 5
        else:
            iteration = len(all_photo)
            
        for i in range(iteration):
            for i2 in range(len(all_photo[i]['sizes'])):
                if height < all_photo[i]['sizes'][i2]['height'] and width < all_photo[i]['sizes'][i2]['width']:
                    height = all_photo[i]['sizes'][i2]['height']
                    width = all_photo[i]['sizes'][i2]['width']
                    url_max = all_photo[i]['sizes'][i2]['url']
                    likes = all_photo[i]['likes']['count']
                    size = all_photo[i]['sizes'][i2]['type']
                    file_name = str(likes) + '.jpg'
                    size_type = str(size)
                    date = all_photo[i]['date']
                    date = datetime.datetime.fromtimestamp(date)
                    date = date.strftime('%Y-%m-%d')
            if file_name in file_name_list:
                file_name = str(f'{likes}{date}.jpg')
            file_name_list.append(file_name)
            photo_dict = [{
                "file_name": file_name,
                "size": size_type
                }]
            ya.create_file_photo(f'Сourse_Work/{file_name}', url_max)
            photo_dict_all.append(photo_dict)
            height = 0
            width = 0
            url_max = ''
            progress_bar()
                
        with open("test.json", "w") as file:
            json.dump(photo_dict_all, file, ensure_ascii=False, indent=2)

def progress_bar():
    mylist = [1,2,3,4,5]
    bar = ShadyBar('Countdown', max = len(mylist))
    for item in mylist:
        bar.next()
        time.sleep(0.1)
    bar.finish()

def logg_str():
    logging.basicConfig(level=logging.DEBUG, filename="py_log.log",filemode="w", format="%(asctime)s %(levelname)s %(message)s")
    logging.debug("A DEBUG Message")
    logging.info("An INFO")
    logging.warning("A WARNING")
    logging.error("An ERROR")
    logging.critical("A message of CRITICAL severity")

logg_str()

id_vk = input('Введите id пользователя vk: ')
token_ya = input('Введите токен с Полигона Яндекс.Диска: ')

ya = YandexDisk(token_ya) # токен с Полигона Яндекс.Диска
ya.create_folder('Сourse_Work')

vkontakte = VK_USER
vkontakte.vk_info(id_vk) # ID id пользователя VK