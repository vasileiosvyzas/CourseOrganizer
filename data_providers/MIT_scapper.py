import requests
import json
import os
from bs4 import BeautifulSoup
from lxml import etree


def get_course_description(course_url):
    course = requests.get(f"https://ocw.mit.edu/{course_url}")

    soup1 = BeautifulSoup(course.content, 'html.parser')

    dom = etree.HTML(str(soup1))
    description = dom.xpath('//*[@id="description"]/div/p/text()')

    return "".join(description)


def topic_related_courses(topic):
    course_list = requests.get(f"https://ocw.mit.edu/courses/find-by-topic/" + topic).json()
    course_info = {}

    for course_data in course_list:
        course_info['course_id'] = course_data['id']
        course_info['course_title'] = course_data['title']
        course_info['course_link'] = f"https://ocw.mit.edu/{course_data['href']}"
        course_info['description'] = get_course_description(course_data['href'])
        course_info['semester'] = course_data['sem']
        course_info['level'] = course_data['level']
        course_info['department'] = course_data['department']


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
