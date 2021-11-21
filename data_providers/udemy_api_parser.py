import requests
import os
import json

from requests.auth import HTTPBasicAuth
from datetime import datetime

client_id = os.environ.get('UDEMY_CLIENT_ID')
client_secret = os.environ.get('UDEMY_SECRET')


def request_courses_list(url):
    courses_list = requests.get(url, auth=HTTPBasicAuth(client_id, client_secret))
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

        write_json(courses, filename)

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


if __name__ == "__main__":
    main()
