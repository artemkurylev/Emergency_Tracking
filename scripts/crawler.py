import argparse
from sources_classes import Springer, Scholar, ACM

SEARCH_TITLE_CLASSES = {'acm': 'issue-item__title', 'scholar': 'gs_rt', 'springer': 'title'}
SEARCH_ABSTRACT_CLASSES = {'acm': 'issue-item__title'}
SEARCH_LINKS = {'acm': 'https://dl.acm.org/action/doSearch?AllField=',
                'scholar': 'https://scholar.google.com/scholar?as_ylo=2016&q=',
                'springer': 'https://link.springer.com/search/page/1?query='}
additional_args = {'acm': {'features': "lxml"}, 'scholar':  {'features': "lxml"}, 'springer': {'features': "lxml"}}

search_sources = {'springer': Springer, 'scholar': Scholar, 'acm': ACM}


class Searcher:
    def __init__(self, source, filename, query, n_pages=1):
        self.source = search_sources[source](filename, query, n_pages)

    def search(self):
        return self.source.search()


def save_text_file(filename, text_lines):

    with open(filename, 'w') as wf:
        wf.writelines(text_lines)
        wf.close()


def main(source, query, filename='default.txt', abstract=False, n_pages=1):
    query_string = ''
    for word in query:
        query_string += word + '+'
    searcher = Searcher(source, filename, query, n_pages)
    titles = searcher.search()
    # Get titles from the first page

    save_text_file(filename, titles)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download some useful info from')
    parser.add_argument('--source', dest='source', default='acm', type=str)
    parser.add_argument('--query', dest='query', type=str, nargs='+')
    parser.add_argument('--filename', dest='filename', default='default.txt')
    parser.add_argument('--npages', dest='n_pages', default=False, type=int)
    parser.add_argument('--abstract', dest='abstract', default=False, type=bool)
    args = parser.parse_args()
    main(args.source, args.query, args.filename, args.abstract, args.n_pages)
