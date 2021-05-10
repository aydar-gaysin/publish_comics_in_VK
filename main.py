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
    api_response = response.json()
    image_url = api_response
    image_response = requests.get(image_url['img'])
    message = image_url['alt']
    image_response.raise_for_status()
    with open(f'xkcd_{random_comics_id}.png', 'wb') as file:
        file.write(image_response.content)
    return message


def request_upload_url(access_token, vk_group_id, vk_api_url):
    parameters = {
        'group_id': vk_group_id,
        'access_token': access_token,
        'v': '5.130'
    }
    vk_api_method = 'photos.getWallUploadServer'
    response = requests.get(f'{vk_api_url}{vk_api_method}', params=parameters)
    response.raise_for_status()
    upload_url = response.json()['response']['upload_url']
    return upload_url


def upload_photo_to_server(random_comics_id, upload_url):
    with open(f'xkcd_{random_comics_id}.png', 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
    api_response = response.json()
    return api_response


def save_uploaded_photo(
        access_token, vk_group_id, vk_api_url, image_server, image_hash,
        image_photo
):
    parameters = {
        'access_token': access_token,
        'group_id': vk_group_id,
        'photo': image_photo,
        'server': image_server,
        'hash': image_hash,
        'v': '5.130'
    }
    vk_api_method = 'photos.saveWallPhoto'
    response = requests.post(f'{vk_api_url}{vk_api_method}', params=parameters)
    response.raise_for_status()
    api_response = response.json()
    return api_response['response'][0]


def post_comics(
        access_token, vk_group_id, vk_api_url, title, media_id, media_owner_id
):
    parameters = {
        'access_token': access_token,
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
    api_response = response.json()
    return api_response


def main():
    load_dotenv()
    access_token = os.getenv('ACCESS_TOKEN')
    vk_group_id = os.getenv('GROUP_ID')
    random_comics_id = generate_random_comics_id(XKCD_URL, POSTFIX_URL)
    try:
        title = fetch_xkcd_comics(random_comics_id, XKCD_URL, POSTFIX_URL)

        upload_url = request_upload_url(access_token, vk_group_id, VK_API_URL)
        upload_comics = upload_photo_to_server(random_comics_id, upload_url)
        image_server = upload_comics['server']
        image_hash = upload_comics['hash']
        image_photo = upload_comics['photo']
        response = save_uploaded_photo(
            access_token, vk_group_id, VK_API_URL, image_server, image_hash,
            image_photo)
        media_id = response['id']
        media_owner_id = response['owner_id']
        post_comics(access_token, vk_group_id, VK_API_URL, title, media_id,
                    media_owner_id)
    except requests.exceptions.HTTPError as error:
        exit('Ошибка:\n{0}'.format(error))
    finally:
        os.remove(f'xkcd_{random_comics_id}.png')


if __name__ == '__main__':
    main()
