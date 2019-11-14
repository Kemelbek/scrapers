import os
import shutil


def download(context, data):
    if data['report_url']:
        report_file = context.http.get(data['report_url'])
        mv_file_to_report_dir(data, report_file)
   


def mv_file_to_report_dir(data, report_file):
    company_url_name = data['company_url'].split('/')[-1]
    create_report_dir(company_url_name)
    shutil.move(report_file.file_path,
                f'{os.getcwd()}/reports/{company_url_name}/{report_file.content_hash}.pdf')



def create_report_dir(company_url_name):
    path = f'{os.getcwd()}/reports/{company_url_name}'
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
