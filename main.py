import logging
import os
import random
import requests

from dotenv import load_dotenv
from urllib.error import HTTPError

XKCD_URL = 'https://xkcd.com/'
POSTFIX_URL = '/info.0.json'
VK_API_URL = 'https://api.vk.com/method/'


def check_api_response(response):
    response.raise_for_status()
    response_content = response.json()
    if "error" in response_content:
        raise requests.HTTPError(response_content["error"]["error_msg"])
    return response_content


def generate_random_comics_id(xkcd_url, postfix_url):
    full_url = f'{xkcd_url}{postfix_url}'
    response = requests.get(full_url)
    response.raise_for_status()
    last_image_id = response.json()['num']
    random_id = random.randint(1, last_image_id)
    return random_id


def fetch_xkcd_comics(random_comics_id, xkcd_url, postfix_url):
    full_url = f'{xkcd_url}{random_comics_id}{postfix_url}'
    response = requests.get(full_url)
    response.raise_for_status()
    random_comic_response = response.json()
    image_response = requests.get(random_comic_response['img'])
    image_response.raise_for_status()
    message = random_comic_response['alt']
    comics_file_name = f'xkcd_{random_comics_id}.png'
    with open(comics_file_name, 'wb') as file:
        file.write(image_response.content)
    return message, comics_file_name


def request_upload_url(vk_implicit_flow_token, vk_group_id, vk_api_url):
    parameters = {
        'group_id': vk_group_id,
        'access_token': vk_implicit_flow_token,
        'v': '5.130'
    }
    vk_api_method = 'photos.getWallUploadServer'
    response = requests.get(f'{vk_api_url}{vk_api_method}', params=parameters)
    return check_api_response(response)['response']['upload_url']


def upload_photo_to_server(comics_file_name, upload_url):
    with open(comics_file_name, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
    return check_api_response(response)


def save_uploaded_photo(
        vk_implicit_flow_token, vk_group_id, vk_api_url, image_server,
        image_hash, image_photo
):
    parameters = {
        'access_token': vk_implicit_flow_token,
        'group_id': vk_group_id,
        'photo': image_photo,
        'server': image_server,
        'hash': image_hash,
        'v': '5.130'
    }
    vk_api_method = 'photos.saveWallPhoto'
    response = requests.post(f'{vk_api_url}{vk_api_method}', params=parameters)
    return check_api_response(response)['response'][0]


def post_comics(
        vk_implicit_flow_token, vk_group_id, vk_api_url, title, media_id,
        media_owner_id
):
    parameters = {
        'access_token': vk_implicit_flow_token,
        'owner_id': f'-{vk_group_id}',
        'attachments': f'photo{media_owner_id}_{media_id}',
        'from_group': 1,
        'group_id': vk_group_id,
        'message': title,
        'v': '5.130'
    }
    vk_api_method = 'wall.post'
    response = requests.post(f'{vk_api_url}{vk_api_method}', params=parameters)
    return check_api_response(response)


def main():
    logging.basicConfig(format='{message}', level=logging.INFO, style='{')
    load_dotenv()
    vk_implicit_flow_token = os.getenv('VK_IMPLICIT_FLOW_TOKEN')
    vk_group_id = os.getenv('GROUP_ID')
    random_comics_id = generate_random_comics_id(XKCD_URL, POSTFIX_URL)
    title, comics_file_name = fetch_xkcd_comics(
        random_comics_id, XKCD_URL, POSTFIX_URL
    )
    try:
        upload_url = request_upload_url(
            vk_implicit_flow_token, vk_group_id, VK_API_URL
        )
        upload_comics = upload_photo_to_server(comics_file_name, upload_url)
        image_server = upload_comics['server']
        image_hash = upload_comics['hash']
        image_photo = upload_comics['photo']
        response = save_uploaded_photo(
            vk_implicit_flow_token, vk_group_id, VK_API_URL, image_server,
            image_hash, image_photo)
        media_id = response['id']
        media_owner_id = response['owner_id']
        post_comics(vk_implicit_flow_token, vk_group_id, VK_API_URL, title,
                    media_id, media_owner_id)
        logging.info('Done!')
    except HTTPError:
        return
    finally:
        os.remove(comics_file_name)


if __name__ == '__main__':
    main()
