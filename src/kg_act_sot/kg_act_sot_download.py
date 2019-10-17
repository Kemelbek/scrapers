import os
import shutil


def download(context, data):
    act_file = context.http.get(data['act_file_url'], lazy=True)
    mv_file_to_act_dir(data, act_file)


def mv_file_to_act_dir(data, act_file):
    case_url_number = data['case_url'].split('/')[-1]
    create_act_dir(case_url_number)
    shutil.move(act_file.file_path, f'{os.getcwd()}/acts/{case_url_number}/{act_file.content_hash}.pdf')


def create_act_dir(case_url_number):
    path = f'{os.getcwd()}/acts/{case_url_number}'
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
