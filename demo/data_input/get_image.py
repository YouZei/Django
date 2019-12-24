from utils import data_read
import requests

def download_img(url,image_name):
    """
    返回图片
    :param url:
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    img = response.content

    image_name = image_name.replace("/", "-").replace("/n", "").replace("\\", "").replace(":", "").replace("*","").replace("?", "")  # 去除非法字符

    with open('./images/%s.jpg' % (image_name), 'wb') as file:
        file.write(img)
        print(image_name, 'Save Successful!')


if __name__ == '__main__':
    data_list = data_read("yg.csv")
    for item in data_list:
        download_img(item["image_url"],item["name"])
