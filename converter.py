#!/Users/zach/Desktop/zvmac/materials/sw/lang/html-css/m2h/venv/bin/python3

from argparse import ArgumentParser
import fileinput
from sys import argv, exit

from bs4 import BeautifulSoup as Soup
from loguru import logger
import markdown2


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", help="Markdown file to convert")
    parser.add_argument("-c", "--chart", help="add chart")
    if len(argv) == 1:
        parser.print_help()
        exit()
    return parser.parse_args()


def convert_to_html(markdown):
    return markdown2.markdown(markdown, extras=["fenced-code-blocks"])


def write_html(filename, content):
    base_name, _ = filename.split('.')
    with open('{}.html'.format(base_name), 'w') as f:
        f.write(content)
    return '{}.html'.format(base_name)


def parse_html(filename):
    with open(filename) as f:
        return Soup(f, "html.parser")


def add_css(html):
    header = html.find("h2")
    link = html.new_tag("link")
    link["rel"] = "stylesheet"
    link["href"] = "styles.css"
    header.insert_before(link)
    header.insert_before("\n")
    return html


def add_chart(html):
    link = html.find("link")
    img = html.new_tag("img")
    img["src"] = "https://quickchart.io/chart?width=500&height=300"
    link.insert_before(img)
    link.insert_before("\n")
    return html


def fix_ampersand(html):
    with fileinput.FileInput(html, inplace=True) as file:
        for line in file:
            print(line.replace('&amp;', '&'), end='')


def write_soup(filename, content):
    base_name, _ = filename.split('.')
    with open('{}.html'.format(base_name), 'w') as f:
        f.write(str(content))
    return '{}.html'.format(base_name)


args = parse_args()

with open(args.file) as f:
    logger.debug("converting to HTML")
    html = convert_to_html(markdown=f.read())
    logger.debug("writing HTML")
    html_file = write_html(filename=args.file, content=html)
    logger.debug("parsing HTML")
    parsed_html = parse_html(html_file)
    logger.debug("adding CSS link")
    css_html = add_css(html=parsed_html)
    if args.chart:
        logger.debug(f"adding {args.chart}")
        charted_html = add_chart(html=css_html)
        html = write_soup(filename=args.file, content=charted_html)
        fix_ampersand(html)
    else:
        write_soup(filename=args.file, content=css_html)
