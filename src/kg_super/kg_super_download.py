import os
import shutil


def download(context, data):
    if data['image_url']:
        image_file = context.http.get(data['image_url'])
        mv_file_to_image_dir(data, image_file)


def mv_file_to_image_dir(data, image_file):
    news_url_name = data['news_url'].split('/')[-2]
    create_image_dir(news_url_name)
    file_type = data['image_url'].split('.')[-1].lower()
    shutil.move(image_file.file_path,
                f'{os.getcwd()}/images_super/{news_url_name}/{image_file.content_hash}.{file_type}')


def create_image_dir(news_url_name):
    path = f'{os.getcwd()}/images_super/{news_url_name}'
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
