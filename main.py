import os
import requests

DIR_PATH = 'comics'
XKCD_URL = 'https://xkcd.com/'
POSTFIX_URL = '/info.0.json'


def fetch_spacex_last_launch(directory, xkcd_url, postfix_url):
    comic_id = '353'
    full_url = f'{xkcd_url}{comic_id}{postfix_url}'
    response = requests.get(full_url)
    response.raise_for_status()
    api_response = response.json()
    image_url = api_response['img']

    with open(os.path.join(directory, f'xkcd_{comic_id}.png'), 'wb') as \
            file:
        get_image = requests.get(image_url)
        get_image.raise_for_status()
        file.write(get_image.content)


def main():
    os.makedirs(DIR_PATH, exist_ok=True)
    try:
        fetch_spacex_last_launch(DIR_PATH, XKCD_URL, POSTFIX_URL)
    except requests.exceptions.HTTPError as error:
        exit('Ошибка:\n{0}'.format(error))


if __name__ == "__main__":
    main()