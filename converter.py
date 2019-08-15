#!/Users/zach/Desktop/zvmac/materials/sw/za/industry/m2h/venv/bin/python3

from argparse import ArgumentParser
from sys import argv, exit

from bs4 import BeautifulSoup as Soup
from loguru import logger
import markdown2


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-m", "--markdown", help="Markdown file to convert")
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
    link["href"] = "https://cdn.jsdelivr.net/gh/kognise/water.css@latest/dist/light.css"
    header.insert_before(link)
    header.insert_before("\n")
    return html


def write_soup(filename, content):
    base_name, _ = filename.split('.')
    with open('{}.html'.format(base_name), 'w') as f:
        f.write(str(content))
    return '{}.html'.format(base_name)


args = parse_args()

with open(args.markdown) as f:
    logger.debug("converting to HTML")
    html = convert_to_html(markdown=f.read())
    logger.debug("writing HTML")
    html_file = write_html(filename=args.markdown, content=html)
    logger.debug("parsing HTML")
    parsed_html = parse_html(html_file)
    logger.debug("adding CSS link")
    parsed_plus_css = add_css(html=parsed_html)
    logger.debug("adding CSS link")
    write_soup(filename=args.markdown, content=parsed_plus_css)
