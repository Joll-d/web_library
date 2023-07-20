import requests
import chardet

from bs4 import BeautifulSoup as BS

def get_website_image_src(website_link: str) -> str:
    r = requests.get(website_link)
    soup = BS(r.text, 'html.parser')
    icon_link = soup.find("link", rel="shortcut icon")
    if icon_link is None:
        icon_link = soup.find("link", rel="icon")
    website_image_src = icon_link.get("href")
    return website_image_src

def get_website_status_code(website_link: str) -> int:
    try:
        r = requests.get(website_link)
        status_code = r.status_code
    except:
        status_code = 404
    return status_code

def get_book_title(book_title_link: str, book_title_path: str) -> str:
    book_title_path = book_title_path.split(";")

    r = requests.get(book_title_link)
    detected_encoding = chardet.detect(r.content)["encoding"]
    r.encoding = detected_encoding
    html = BS(r.text, 'html.parser')

    element = html

    for element_path in book_title_path:
        element_path = element_path.lstrip()
        element_path = element_path.split(" ")
        element_selector = element_path[0]
        element_class = element_path[1] if len(element_path) == 2 else ""
        element = element.find(element_selector[1:-1], class_=element_class)

    return element.text

def get_image_src(book_title_link: str, art_path: str) -> str:
    art_path = art_path.split(";")

    r = requests.get(book_title_link)
    detected_encoding = chardet.detect(r.content)["encoding"]
    r.encoding = detected_encoding
    html = BS(r.text, 'html.parser')

    element = html

    for element_path in art_path:
        element_path = element_path.lstrip()
        element_path = element_path.split(" ")
        element_selector = element_path[0]
        element_class = element_path[1] if len(element_path) == 2 else ""
        element = element.find(element_selector[1:-1], class_=element_class)

    return element.get('src')


def get_chapter_title(chapter_link: str, chapter_title_path: str) -> str:
    chapter_title_path = chapter_title_path.split(";")

    r = requests.get(chapter_link)
    detected_encoding = chardet.detect(r.content)["encoding"]
    r.encoding = detected_encoding
    html = BS(r.text, 'html.parser')

    element = html

    for element_path in chapter_title_path:
        element_path = element_path.lstrip()
        element_path = element_path.split(" ")
        element_selector = element_path[0]
        element_class = element_path[1] if len(element_path) == 2 else ""
        element = element.find(element_selector[1:-1], class_=element_class)

    chapter_title = element.text
    return chapter_title


def get_chapter_content(chapter_link: str, content_path: str) -> list:
    splited_content_path = content_path.split(";")
    content_path = splited_content_path[:-1]

    paragraph_separator = splited_content_path[-1].split(":")

    r = requests.get(chapter_link)
    detected_encoding = chardet.detect(r.content)["encoding"]
    r.encoding = detected_encoding
    html = BS(r.text, 'html.parser')

    element = html

    for element_path in content_path:
        element_path = element_path.lstrip()
        element_path = element_path.split(" ")
        element_selector = element_path[0]
        element_class = element_path[1] if len(element_path) == 2 else ""
        element = element.find(element_selector[1:-1], class_=element_class)

    separator_type = paragraph_separator[0].strip()
    separator_selector = paragraph_separator[1].strip()
    content =[]
    if separator_type == 'block':
        content = element.find_all(separator_selector)
    elif separator_type == 'spacer':
        content = list(element.stripped_strings)

    return content


def get_page_link(chapter_link: str, book_page_link_path: str) -> str:
    splited_book_page_link_path = book_page_link_path.split(";")
    book_page_link_path = splited_book_page_link_path[:-1]
    link_path = splited_book_page_link_path[-1].strip().split(" ")

    r = requests.get(chapter_link)
    detected_encoding = chardet.detect(r.content)["encoding"]
    r.encoding = detected_encoding
    html = BS(r.text, 'html.parser')

    element = html

    for element_path in book_page_link_path:
        element_path = element_path.lstrip()
        element_path = element_path.split(" ")
        element_selector = element_path[0]
        element_class = element_path[1] if len(element_path) == 2 else ""
        element = element.find(element_selector[1:-1], class_=element_class)

    button_selector = link_path[0].strip()
    button_iterator = link_path[1].strip()
    button_iterator = int(button_iterator[1:-1])
    elements = element.find_all(button_selector[1:-1])
    element = elements[button_iterator-1]

    book_page_link = element.get('href')
    return book_page_link