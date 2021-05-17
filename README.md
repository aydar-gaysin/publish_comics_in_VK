# Публикация комиксов

Read this in: [English](https://github.com/aydar-gaysin/publish_comics_in_VK/blob/master/README.en.md)

Данная программа скачивает случайный комикс с комментарием автора с сайта https://xkcd.com/ и публикует его в вашем
сообществе в социальной сети Вконтакте через API.

Для запуска программы потребуется указать:
1) ID группы```(group_id)``` Вконтакте;
2) Ключ доступа пользователя```(access token)``` API Вконтакте.

### Ссылки на полезные материалы

1. [Создать группу Вконтакте](https://vk.com/dev/vkapp_create)
   
1. [Узнать group_id вашей группы Вконтакте](https://regvk.com/id/)
   
1. [Implicit Flow для получения ключа доступа пользователя](https://vk.com/dev/implicit_flow_user)


### Как установить

У вас должен быть установлен Python3.

1. Скопируйте репозиторий

2. Установите зависимости:
```python
pip install -r requirements.txt
```
3. Создайте ```.env``` файл, укажите ACCESS TOKEN для взаимодействия с API VK, ID вашей группы Вконтакте:
```python
VK_IMPLICIT_FLOW_TOKEN=
GROUP_ID=
``` 
4. Из командной строки запустите *main.py*:
```python
python main.py
```


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков
[dvmn.org](https://dvmn.org/referrals/HmkuFA0LXGDNGGqup2HnEZibxamNJcUwaRvhx5Zt/).
