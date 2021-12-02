import requests
import json
import os
from bs4 import BeautifulSoup

def get_course_info(course_url):
    course = requests.get(f"https://ocw.mit.edu/{course_url}")

    soup1 = BeautifulSoup(course.text, 'lxml')

    description = soup1.find_all('div', {'id': 'description'})




def topic_related_courses(topic):
    course_list = requests.get(f"https://ocw.mit.edu/courses/find-by-topic/" + topic).json()

    for course_info in course_list:
        print(course_info['id'], course_info['title'], course_info['href'])
        get_course_info(course_info['href'])
        break


def main():
    topics_url = 'https://ocw.mit.edu/courses/find-by-topic/topics.json'

    topics = requests.get(topics_url).json()
    for topic in topics:
        print(topic['name'])
        print(topic['file'])
        topic_related_courses(topic['file'])
        break


if __name__ == '__main__':
    main()
