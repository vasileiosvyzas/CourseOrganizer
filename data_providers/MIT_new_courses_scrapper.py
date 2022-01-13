import requests
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup
from lxml import etree


def get_course_level(course_page):
    """
    :param course_page:
    :return: course level as string
    """
    course = requests.get(course_page)

    soup2 = BeautifulSoup(course.content, 'html.parser')

    level_tag = soup2.find('h3', text='Level')

    if level_tag is None:
        return None
    else:
        return level_tag.find_next_sibling('p').text


def main():
    topics_url = 'https://ocw.mit.edu/rss/new/mit-newcourses.xml'
    new_courses = requests.get(topics_url).content
    course_info = {}
    soup1 = BeautifulSoup(new_courses, 'lxml')
    new_courses = soup1.find_all("item")

    course_list = []
    for course in new_courses:
        course_info['title'] = course.title.text
        course_info['description'] = course.description.text
        course_info['url'] = course['rdf:about']
        course_info['semester'] = course.fromsemester.text
        course_info['year'] = course.fromyear.text
        course_info['level'] = get_course_level(course['rdf:about'])

        course_list.append(course_info)

    file_name = str(datetime.now().date()) + '_mit_new_courses.json'
    file_location = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'data', file_name)
    with open(file_location, 'w') as output_file:
        json.dump(course_list, output_file)


if __name__ == '__main__':
    main()
