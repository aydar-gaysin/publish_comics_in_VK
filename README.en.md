# Comics publisher

Read this in: [Русский](https://github.com/aydar-gaysin/publish_comics_in_VK/blob/master/README.md)

This program downloads random comics with author's message from https://xkcd.com/ and publish it in your
[VK](https://vk.com/) public through API.

Before start, please, ensure that you possess the following data:
1) VK Group ID```(group_id)```;
2) VK API user's access key```(access token)```.

### Useful links

1. [Create VK public group](https://vk.com/dev/vkapp_create)
   
1. [Find out the group_id](https://regvk.com/id/)
   
1. [Implicit Flow to obtain VK API user's access key](https://vk.com/dev/implicit_flow_user)

### How to install

You should have Python3 install on your PC.

1. Fork the repo

2. Install the requirements:
```python
pip install -r requirements.txt
```
3. Create ```.env``` file, put ACCESS TOKEN , group_id into it:
```python
VK_IMPLICIT_FLOW_TOKEN=
GROUP_ID=
``` 
4. From terminal start *main.py*:
```python
python main.py
```

### Project Goals

The code is written for educational purposes on online-course for web-developers
[dvmn.org](https://dvmn.org/referrals/HmkuFA0LXGDNGGqup2HnEZibxamNJcUwaRvhx5Zt/).
