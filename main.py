import os
import random
import requests

from dotenv import load_dotenv


XKCD_URL = 'https://xkcd.com/'
POSTFIX_URL = '/info.0.json'
VK_API_URL = 'https://api.vk.com/method/'


def generate_random_comics_id(xkcd_url, postfix_url):
    full_url = f'{xkcd_url}{postfix_url}'
    response = requests.get(full_url)
    response.raise_for_status()
    api_response = response.json()
    last_image_id = api_response['num']
    random_id = random.randint(1, last_image_id)
    return random_id


def fetch_xkcd_comics(random_comics_id, xkcd_url, postfix_url):
    full_url = f'{xkcd_url}{random_comics_id}{postfix_url}'
    response = requests.get(full_url)
    response.raise_for_status()
    image_url = response.json()
    image_response = requests.get(image_url['img'])
    message = image_url['alt']
    image_response.raise_for_status()
    comics_file_name = f'xkcd_{random_comics_id}.png'
    with open(comics_file_name, 'wb') as file:
        file.write(image_response.content)
    return message, comics_file_name


def check_api_response(response):
    try:
        response.json()
        return True
    except requests.exceptions.HTTPError as error:
        exit('Ошибка:\n{0}'.format(error))


def request_upload_url(vk_implicit_flow_token, vk_group_id, vk_api_url):
    parameters = {
        'group_id': vk_group_id,
        'access_token': vk_implicit_flow_token,
        'v': '5.130'
    }
    vk_api_method = 'photos.getWallUploadServer'
    response = requests.get(f'{vk_api_url}{vk_api_method}', params=parameters)
    response.raise_for_status()
    if check_api_response(response):
        upload_url = response.json()['response']['upload_url']
        return upload_url


def upload_photo_to_server(comics_file_name, upload_url):
    with open(comics_file_name, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
    if check_api_response(response):
        api_response = response.json()
        return api_response


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
    response.raise_for_status()
    if check_api_response(response):
        api_response = response.json()
        return api_response['response'][0]


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
    response.raise_for_status()
    if check_api_response(response):
        api_response = response.json()
        return api_response


def main():
    load_dotenv()
    vk_implicit_flow_token = os.getenv('VK_IMPLICIT_FLOW_TOKEN')
    vk_group_id = os.getenv('GROUP_ID')
    try:
        random_comics_id = generate_random_comics_id(XKCD_URL, POSTFIX_URL)
        title, comics_file_name = fetch_xkcd_comics(
            random_comics_id, XKCD_URL, POSTFIX_URL
        )
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
    finally:
        os.remove(comics_file_name)


if __name__ == '__main__':
    main()
