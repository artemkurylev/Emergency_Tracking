from bs4 import BeautifulSoup as bs
from abc import ABC, abstractmethod
import requests
import json

SEARCH_TITLE_CLASSES = {'acm': 'issue-item__title', 'scholar': 'gs_rt', 'springer': 'title'}
SEARCH_ABSTRACT_CLASSES = {'acm': 'issue-item__title'}
SEARCH_LINKS = {'acm': 'https://dl.acm.org/action/doSearch?AllField=',
                'scholar': 'https://scholar.google.com/scholar?as_ylo=2016&q=',
                'springer': 'https://link.springer.com/search/page/1?query='}
additional_args = {'acm': {'features': "lxml"}, 'scholar':  {'features': "lxml"}, 'springer': {'features': "lxml"}}


class Source(ABC):
    def __init__(self, filename, query, n_pages, source_type):

        self.query = ''
        for word in query:
            self.query += word + '+'
        self.n_pages = n_pages
        self.search_link = SEARCH_LINKS[source_type] + self.query
        self.search_class = SEARCH_TITLE_CLASSES[source_type]
        self.titles = []
        self.filename = filename

    @abstractmethod
    def search(self):
        return []

    def write_json_to_file(self):
        with open(self.filename, 'w') as wf:
            json.dump(self.titles, wf)


class Scholar(Source):
    def __init__(self, filename, query, n_pages=1):
        super(Scholar, self).__init__(filename, query, n_pages, 'scholar')

    def search(self):
        title_classes = []
        for i in range(self.n_pages):
            start = i * 10 if i > 0 else 0
            if i > 0:
                self.search_link += f'&start={start}'
            page = requests.get(self.search_link)
            html_page = bs(page.text, **additional_args['scholar'])
            print(html_page)
            title_classes += Scholar.search_scholar_page(html_page, self.search_class)
            print(len(title_classes))
        self.titles = [{'Name': title.text, 'Link': title.get("href")} for idx, title in
                  enumerate(title_classes)]
        self.write_json_to_file()

    @staticmethod
    def search_scholar_page(html_page, search_class):
        title_classes = html_page.findAll(class_=search_class)
        titles = []
        for title_object in title_classes:
            title = title_object.find('a')
            titles.append(title)

        return titles


class Springer(Source):
    def __init__(self, filename, query, n_pages=1):
        super(Springer, self).__init__(filename, query, n_pages, 'springer')

    def search(self):
        title_objects = []
        for i in range(self.n_pages):
            page_num = i + 1
            if i > 1:
                self.search_link.replace('1', str(page_num))
            page = requests.get(self.search_link)
            html_page = bs(page.text, **additional_args['springer'])
            title_objects += Springer.search_springer_page(html_page, self.search_class)
        self.titles = [{'Name': title.text, 'Link': title.get("href")} for idx, title in
                       enumerate(title_objects)]
        self.write_json_to_file()

    @staticmethod
    def search_springer_page(html_page, search_class):
        title_classes = html_page.findAll(class_=search_class)
        titles = []
        for title_object in title_classes:
            titles.append(title_object)
        return titles


class ACM(Source):
    def __init__(self, filename, query, n_pages=1):
        super(ACM, self).__init__(filename, query, n_pages, 'acm')

    def search(self):
        title_classes = []
        for i in range(self.n_pages):
            startPage = i
            if i > 0:
                self.search_link += f'startPage={startPage}'
            page = requests.get(self.search_link)
            html_page = bs(page.text, **additional_args['acm'])
            title_classes += ACM.search_acm_page(html_page, self.search_class)
        self.titles = [{'Name': title.text, 'Link': title.find("a").get("href")} for idx, title in
                       enumerate(title_classes)]
        self.write_json_to_file()

    @staticmethod
    def search_acm_page(html_page, search_class):
        title_classes = html_page.findAll(class_=search_class)
        titles = []
        for title_object in title_classes:
            titles.append(title_object)
        return titles
