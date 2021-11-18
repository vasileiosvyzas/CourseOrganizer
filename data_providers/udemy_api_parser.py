import requests
import os
import json

from requests.auth import HTTPBasicAuth
from datetime import datetime

client_id = 'nzCKl5gJKWcSoXXnNU5RB6XXNyeColzpwEAfapaA'
client_secret = 'dROYzyuO7IpEi8nE9fyUbrECowtuCfxHodoCQ53PgB7dg2JFblpSrVz4tsjjfmCYNbOtAIT9bEnYKderbVSAyK7ucLOIRfaxwmHtZ0pkfl90zqtUUikHiOn6DJ1gfpso'


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
        file_data["results"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


def get_data_from_new_page_and_write_to_file(page, filename):
    if page is not None:
        courses_list = request_courses_list(page)
        for result in courses_list['results']:
            print(result)
            write_json(result, filename)
        page = get_next_page(courses_list)
        get_data_from_new_page_and_write_to_file(page,
                                                 os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)),
                                                              'data', filename))


def main():
    root_endpoint = 'https://www.udemy.com/api-2.0/courses/'
    courses_list = request_courses_list(root_endpoint)

    file_name = str(datetime.now().date()) + '.json'
    with open(os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'data', file_name),
              'w') as outputfile:
        json.dump(courses_list, outputfile)

    page = get_next_page(courses_list)
    print(page)
    if page is not None:
        get_data_from_new_page_and_write_to_file(page,
                                                 os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)),
                                                              'data', file_name))


if __name__ == "__main__":
    main()
