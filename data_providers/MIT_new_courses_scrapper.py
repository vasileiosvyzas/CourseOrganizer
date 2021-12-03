import requests
import json
import os
from datetime import datetime
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
    course_info_list = []
    for course_data in course_list:
        course_info['course_id'] = course_data['id']
        course_info['course_title'] = course_data['title']
        course_info['course_link'] = f"https://ocw.mit.edu/{course_data['href']}"
        course_info['description'] = get_course_description(course_data['href'])
        course_info['semester'] = course_data['sem']
        course_info['level'] = course_data['level']
        course_info['department'] = course_data['department']

        course_info_list.append(course_info)

    return course_info_list


def write_json(new_data, filename):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)

        # Join new_data with file_data inside emp_details
        file_data.extend(new_data)

        # Sets file's current position at offset.
        file.seek(0)

        # convert back to json.
        json.dump(file_data, file, indent=4)


def main():
    topics_url = 'https://ocw.mit.edu/rss/new/mit-newcourses.xml'
    new_courses = requests.get(topics_url).content

    soup1 = BeautifulSoup(new_courses, 'lxml')



if __name__ == '__main__':
    main()
