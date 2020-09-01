import json
from pathlib import Path
import argparse


def remove_duplicates(titles):
    unique_titles = {}
    for title in titles:
        name = title['Name']
        if name not in unique_titles:
            unique_titles[name] = title['Link']
    return unique_titles


def aggregate_titles(path_to_files, out_path):
    path = Path(path_to_files)
    all_files = path.glob('*.txt')
    titles = []
    for file in all_files:
        with open(file, 'r') as rf:
            titles += json.load(rf)
    unique_titles = remove_duplicates(titles)
    titles_string = [f'{idx + 1}) Name: {title}\n\n Link: {unique_titles[title]} \n\n' for idx, title in
                     enumerate(unique_titles)]
    with open(out_path, 'w') as wf:
        wf.writelines(titles_string)


def main(path_to_files, out_path):
    aggregate_titles(path_to_files, out_path)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filtering of received articles')
    parser.add_argument('--path', dest='files_path', default='../article_titles', type=str)
    parser.add_argument('--output_path', dest='out_path', default='filtered_titles.txt', type=str)
    args = parser.parse_args()
    main(args.files_path, args.out_path)
