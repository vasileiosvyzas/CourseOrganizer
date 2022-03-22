import os
import json
from datetime import datetime, timedelta

from airflow import DAG
from requests.auth import HTTPBasicAuth
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from typing import Dict, List


def request_courses_list(url, session) -> Dict:
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


def get_courses_from_all_pages():
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


with DAG(
        'udemy_course_parser',
        default_args={
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5)
        },
        description='A DAG that gets the courses from the Udemy API',
        schedule_interval='@once',
        start_date=days_ago(1),
        catchup=False,
) as dag:
    python_task = PythonOperator(task_id='get_courses_list', python_callable=get_courses_from_all_pages)
