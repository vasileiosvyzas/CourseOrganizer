import requests
import os
import json
import boto3

from typing import Dict, List
from requests.auth import HTTPBasicAuth
from datetime import datetime


def request_courses_list(url: str, session) -> Dict:
    try:
        response = session.get(url,
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


def write_data_to_json_on_disk(courses: List, file_location: str) -> None:
    with open(file_location, 'w') as output_file:
        json.dump(courses, output_file)


def upload_courses_list_file_to_s3_bucket(file_location: str, filename: str) -> None:
    """
    It takes the filename of the json file with all the courses and it will upload it to
    the S3 bucket
    :param filename:
    :param file_location:
    :return:
    """
    try:
        print('uploading to s3')
        session = boto3.Session(profile_name='iamadmin-portofolio-general')
        s3_resource = session.resource('s3')
        s3_resource.Bucket('udemy-courses-store').upload_file(file_location, filename)
    except Exception as e:
        print(e)
        print('something went wrong')


def main():
    session = requests.Session()
    root_endpoint = 'https://www.udemy.com/api-2.0/courses/'
    courses_list = request_courses_list(root_endpoint, session)

    all_courses = courses_list['results']
    while courses_list['next'] is not None:
        next_page = courses_list['next']
        print(next_page)
        courses_list = request_courses_list(next_page, session)
        all_courses.extend(courses_list['results'])

    file_name = str(datetime.now().date()) + '.json'
    file_location = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'data', file_name)

    write_data_to_json_on_disk(courses=all_courses, file_location=file_location)

    print(file_location)
    upload_courses_list_file_to_s3_bucket(file_location=file_location, filename=file_name)


if __name__ == "__main__":
    main()
