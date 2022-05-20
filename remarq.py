#!/usr/bin/env python

import argparse
import sys
import time

from text_processor import (
    process_text,
    print_text,
    print_stat,
)
from util.file import (
    is_path,
    get_file_contents,
)
from util.word_lists import complex_phrases


def main():
    # TODO(redd4ford): turn this project into a command-line tool
    # TODO(redd4ford): provide CLI for in-terminal file editing and creation
    try:
        parser = argparse.ArgumentParser(description='A text readability analyzer.')
        parser.add_argument(
            '-p', '--path', type=is_path, help='specify the text file\'s path'
        )
        parser.add_argument(
            '--example', action='store_true', help='use an example file to demonstrate the power of remarq'
        )
        args = parser.parse_args()

        filepath = 'example.txt' if args.example else args.path
        text = get_file_contents(filepath)

        start_time = time.time()
        processed_text, text_stat = process_text(text)
        print_text(processed_text)
        print_stat()
        print("--- %s seconds ---" % (time.time() - start_time))

        # TODO(redd4ford): provide better CLI
        while True:
            try:
                word = input('> ')
                if word.lower() in complex_phrases:
                    print(f'# {", ".join(complex_phrases[word.lower()])}')
                else:
                    print(f'# no results')
            except KeyboardInterrupt:
                print('Exiting...')
                time.sleep(1)
                break
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    main()
