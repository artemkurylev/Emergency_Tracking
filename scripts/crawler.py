import requests
import sys
import argparse
from bs4 import BeautifulSoup as bs

SEARCH_TITLE_CLASSES = {'acm': 'issue-item__title', 'scholar': 'gs_rt', 'springer': 'title'}
SEARCH_ABSTRACT_CLASSES = {'acm': 'issue-item__title'}
SEARCH_LINKS = {'acm': 'https://dl.acm.org/action/doSearch?AllField=',
                'scholar': 'https://scholar.google.com/scholar?as_ylo=2016&q=',
                'springer': 'https://link.springer.com/search?query='}
additional_args = {'acm': {'features': "lxml"}, 'scholar':  {'features': "lxml"}, 'springer': {'features': "lxml"}}


def save_text_file(filename, text_lines):

    with open(filename, 'w') as wf:
        wf.writelines(text_lines)
        wf.close()


def search_scholar_page(html_page, search_class):
    title_classes = html_page.findAll(class_=search_class)
    titles = []
    for title_object in title_classes:
        title = title_object.find('a')
        titles.append(title)
    return titles


def search_springer_page(html_page, search_class):
    title_classes = html_page.findAll(class_=search_class)
    titles = []
    for title_object in title_classes:
        titles.append(title_object)
    return titles


def main(source, query, filename='default.txt', abstract=False):
    query_string = ''
    for word in query:
        query_string += word + '+'
    search_class = SEARCH_TITLE_CLASSES[source]
    search_link = SEARCH_LINKS[source]

    query_string = query_string[:-1]
    request_addr = search_link + query_string
    page = requests.get(request_addr)
    html_page = bs(page.text, **additional_args[source])

    if source == 'scholar':
        title_classes = search_scholar_page(html_page, search_class)
        titles = [f'{idx + 1}) Name: {title.text} \n\n Link: {title.get("href")} \n\n' for idx, title in
                  enumerate(title_classes)]
    elif source == 'springer':
        title_classes = search_springer_page(html_page, search_class)
        titles = [f'{idx + 1}) Name: {title.text} \n\n Link: {title.get("href")} \n\n' for idx, title in
                  enumerate(title_classes)]
    else:
        title_classes = html_page.findAll(class_=search_class)

        titles = [f'{idx + 1}) Name: {title.text} \n\n Link: {title.find("a").get("href")} \n\n' for idx, title in
                  enumerate(title_classes)]

    # Get titles from the first page

    save_text_file(filename, titles)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download some useful info from')
    parser.add_argument('--source', dest='source', default='acm', type=str)
    parser.add_argument('--query', dest='query', type=str, nargs='+')
    parser.add_argument('--filename', dest='filename', default='default.txt')
    parser.add_argument('--abstract', dest='abstract', default=False, type=bool)
    args = parser.parse_args()
    main(args.source, args.query, args.filename, args.abstract)
