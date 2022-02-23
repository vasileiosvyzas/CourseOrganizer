import requests
import os
import json
import boto3

from typing import Dict, List
from requests.auth import HTTPBasicAuth
from datetime import datetime


def request_courses_list(url: str) -> Dict:
    try:
        response = requests.get(url,
                                auth=HTTPBasicAuth(os.environ.get('UDEMY_CLIENT_ID'),
                                                   os.environ.get('UDEMY_SECRET')))

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)


# def get_next_page(courses_list):
#     if courses_list['next'] is not None:
#         return courses_list['next']
#     else:
#         return None


# def write_json(new_data, filename):
#     with open(filename, 'r+') as file:
#         # First we load existing data into a dict.
#         file_data = json.load(file)
#
#         # Join new_data with file_data inside emp_details
#         file_data['results'].extend(new_data)
#
#         # Sets file's current position at offset.
#         file.seek(0)
#
#         # convert back to json.
#         json.dump(file_data, file, indent=4)


# def get_data_from_new_page_and_write_to_file(page, filename):
#     if page is not None:
#         courses_list = request_courses_list(page)
#         courses = courses_list['results']
#
#         print('Updating the json')
#         write_json(courses, filename)
#
#         print('Getting the new page and start all over again')
#         page = get_next_page(courses_list)
#         get_data_from_new_page_and_write_to_file(page, filename)
#     else:
#         print('Reached the end of pages')

def write_data_to_json_on_disk(courses_list: List) -> None:
    file_name = str(datetime.now().date()) + '.json'
    file_location = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'data', file_name)

    with open(file_location, 'w') as output_file:
        json.dump(courses_list, output_file)


def main():
    root_endpoint = 'https://www.udemy.com/api-2.0/courses/'
    courses_list = request_courses_list(root_endpoint)

    all_courses = courses_list['results']
    result = 0
    while courses_list['next'] is not None:
        next_page = courses_list['next']
        courses_list = request_courses_list(next_page)
        all_courses.extend(courses_list['results'])

    write_data_to_json_on_disk(all_courses)


if __name__ == "__main__":
    main()
