import requests
import chardet

from bs4 import BeautifulSoup as BS


class BookParser:

    def __init__(self, website_link) -> None:
        self._website_link = website_link
     
    def get_website_icon_src(self) -> str:
        r = requests.get(self._website_link)
        soup = BS(r.text, 'html.parser')
        icon_link = soup.find("link", rel="shortcut icon")
        if icon_link is None:
            icon_link = soup.find("link", rel="icon")
        website_image_src = self._get_full_url(icon_link.get("href"))
        return website_image_src

    def get_website_status_code(self) -> int:
        try:
            r = requests.get(self._website_link)
            status_code = r.status_code
        except:
            status_code = 404
        return status_code

    def get_element_text(self, book_title_path: str) -> str:
        book_title_path = book_title_path.split(";")

        r = requests.get(self._website_link)
        detected_encoding = chardet.detect(r.content)["encoding"]
        r.encoding = detected_encoding
        html = BS(r.text, 'html.parser')

        element = self._get_element_by_path(html, book_title_path)

        return element.text

    def get_element_src(self, element_path: str) -> str:
        element_path = element_path.split(";")

        r = requests.get(self._website_link)
        detected_encoding = chardet.detect(r.content)["encoding"]
        r.encoding = detected_encoding
        html = BS(r.text, 'html.parser')

        element = self._get_element_by_path(html, element_path)

        return element.get('src')

    def get_elements_text(self, parent_element_path: str) -> list:
        parent_element_path = parent_element_path.split(";")

        r = requests.get(self._website_link)
        detected_encoding = chardet.detect(r.content)["encoding"]
        r.encoding = detected_encoding
        html = BS(r.text, 'html.parser')

        element = self._get_element_by_path(html, parent_element_path)

        content = list(element.stripped_strings)
        return content

    def get_element_href(self, element_href_path: str) -> str:
        element_href_path = element_href_path.split(";")

        r = requests.get(self._website_link)
        detected_encoding = chardet.detect(r.content)["encoding"]
        r.encoding = detected_encoding
        html = BS(r.text, 'html.parser')

        element = self._get_element_by_path(html, element_href_path)

        if element is None:
            return element
        else:
            book_page_link = self._get_full_url(element.get('href'))
        return book_page_link
           
    def _get_element_orderly_number(self, element_class: str) -> tuple[str, int]:
        element_orderly_number = 0

        if element_class.find('[') != -1:
            element_orderly_number_coordinates = [element_class.find('['), element_class.find(']')]
            element_orderly_number = int(element_class[element_orderly_number_coordinates[0]+1:element_orderly_number_coordinates[1]])
            element_class = element_class.replace(f'[{element_orderly_number}]', '')

        return element_class.strip(), element_orderly_number

    def _get_element_by_path(self, html: BS, element_full_path: list) -> BS:
        element = html
        element_full_path = [element.strip() for element in element_full_path]

        for element_path in element_full_path:
            element_selector_end = element_path.find(" ")
            element_selector = element_path[1:element_selector_end-1] if element_selector_end != -1 else element_path[1:-1]
            element_class = element_path[element_selector_end:].strip() if element_selector_end != -1 else ""

            element_class, element_orderly_number = self._get_element_orderly_number(element_class)

            optional = False
            if element_class.find('`OP') != -1:
                element_class = element_class.replace('`OP', '').strip()
                optional = True

            try:
                if element_class == '':
                    element = element.find_all(element_selector)
                else:
                    element = element.find_all(element_selector, class_=element_class)
                
                element = element[element_orderly_number]
            except:
                if optional:
                    return None


        return element

    def _get_full_url(self, shortened_url: str):
        url = shortened_url
        if shortened_url.find('://') == -1:
            domain_start = self._website_link.find("://") + 3
            domain_end = self._website_link.find("/", domain_start)
            url = self._website_link[:domain_end] + shortened_url
        return url