import requests
import json
import os
from bs4 import BeautifulSoup


def main():
    topics_url = 'https://ocw.mit.edu/courses/find-by-topic/topics.json'

    topics = requests.get(topics_url).json()
    for topic in topics:
        print(topic)


if __name__ == '__main__':
    main()