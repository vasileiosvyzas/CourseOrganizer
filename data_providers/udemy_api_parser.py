import requests
import os
import json
import boto3

from requests.auth import HTTPBasicAuth
from datetime import datetime


def request_courses_list(url):
    courses_list = requests.get(url,
                                auth=HTTPBasicAuth(os.environ.get('UDEMY_CLIENT_ID'),
                                                   os.environ.get('UDEMY_SECRET')))
    return courses_list.json()


def get_next_page(courses_list):
    if courses_list['next'] is not None:
        return courses_list['next']
    else:
        return None


def write_json(new_data, filename):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)

        # Join new_data with file_data inside emp_details
        file_data['results'].extend(new_data)

        # Sets file's current position at offset.
        file.seek(0)

        # convert back to json.
        json.dump(file_data, file, indent=4)


def get_data_from_new_page_and_write_to_file(page, filename):
    if page is not None:
        courses_list = request_courses_list(page)
        courses = courses_list['results']

        print('Updating the json')
        write_json(courses, filename)

        print('Getting the new page and start all over again')
        page = get_next_page(courses_list)
        get_data_from_new_page_and_write_to_file(page, filename)
    else:
        print('Reached the end of pages')


def main():
    root_endpoint = 'https://www.udemy.com/api-2.0/courses/'
    courses_list = request_courses_list(root_endpoint)

    file_name = str(datetime.now().date()) + '.json'
    file_location = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'data', file_name)

    with open(file_location, 'w') as output_file:
        json.dump(courses_list, output_file)

    page = get_next_page(courses_list)
    get_data_from_new_page_and_write_to_file(page, file_location)

    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-1',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    name_of_file = os.path.basename(file_name)
    s3.create_bucket(Bucket='portfolio-udemy-data')

    s3.Bucket('portfolio-udemy-data').upload_file(Filename=file_location, Key='udemy/' + name_of_file)
    print('bucket has been created and data were added')


if __name__ == "__main__":
    main()
