#!/Users/zach/Desktop/zvmac/materials/sw/za/industry/m2h/venv/bin/python3

from sys import argv

from bs4 import BeautifulSoup as Soup
from loguru import logger


def add_css(parsed):
    header = parsed.find("h1")
    link = parsed.new_tag("link")
    link["rel"] = "stylesheet"
    link["href"] = "https://cdn.jsdelivr.net/gh/kognise/water.css@latest/dist/light.css"
    header.insert_before(link)
    header.insert_before("\n")
    return parsed


with open(argv[1]) as f:
    logger.debug("ready to parse 🗃  {}".format(argv[1]))
    parsed_file = Soup(f, "html.parser")
    parsed_plus_css = add_css(parsed_file)
    logger.debug("HTML to write ✍🏼 \n\n  {}".format(parsed_file))
