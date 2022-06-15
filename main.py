import json
from vk_get_photo import VK_users
from upload_to_ya_disk import YaUploader


def create_json_file():
    res = vk_res
    with open('photo.json', 'w', encoding='utf-8') as outfile:
        json.dump(res[1], outfile)


if __name__=='__main__':
    vk_res = VK_users.vk_main(None)
    create_json_file()
    YaUploader.ya_main(None, vk_res)
