import os
import requests

from dotenv import load_dotenv


DIR_PATH = 'comics'
XKCD_URL = 'https://xkcd.com/'
POSTFIX_URL = '/info.0.json'
VK_API_URL = 'https://api.vk.com/method/'


def fetch_spacex_last_launch(directory, xkcd_url, postfix_url):
    comic_id = '353'
    full_url = f'{xkcd_url}{comic_id}{postfix_url}'
    response = requests.get(full_url)
    response.raise_for_status()
    api_response = response.json()
    image_url = api_response

    with open(os.path.join(directory, f'xkcd_{comic_id}.png'), 'wb') as \
            file:
        get_image = requests.get(image_url['img'])
        print(image_url['alt'])
        get_image.raise_for_status()
        file.write(get_image.content)


def request_upload_url(access_token, vk_group_id, vk_api_url):
    parameters = {
        'group_id': vk_group_id,
        'access_token': access_token,
        'v': '5.130'
    }
    vk_api_method = 'photos.getWallUploadServer'
    response = requests.get(f'{vk_api_url}{vk_api_method}', params=parameters)
    response.raise_for_status()
    get_upload_url = response.json()['response']['upload_url']
    return get_upload_url


def main():
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    access_token = os.getenv('ACCESS_TOKEN')
    vk_group_id = os.getenv('GROUP_ID')
    # os.makedirs(DIR_PATH, exist_ok=True)
    # try:
    #     fetch_spacex_last_launch(DIR_PATH, XKCD_URL, POSTFIX_URL)
    # except requests.exceptions.HTTPError as error:
    #     exit('Ошибка:\n{0}'.format(error))
    response = request_upload_url(access_token, vk_group_id, VK_API_URL)
    print(response)


if __name__ == "__main__":
    main()