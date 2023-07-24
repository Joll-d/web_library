def get_domain_from_link(link: str) -> str:
    domain_start = link.find("://") + 3
    domain_end = link.find("/", domain_start)
    domain = link[domain_start:domain_end] 
    return domain


def get_website_name_from_link(link: str) -> str:
    name = link.split('.')
    return name[1]


def get_book_title_page_length(book_title_page_link: str) -> int:
    book_title_page_length = book_title_page_link.split("/")
    return len(book_title_page_length)


def get_book_title_page_link_supplement(book_title_page_link: str, book_chapter_page_link: str) -> str:
    splited_book_title_page_link = book_title_page_link.split("/")
    splited_book_chapter_page_link = book_chapter_page_link.split("/")

    last_title_part_of_chapter_page_link = splited_book_title_page_link[len(splited_book_title_page_link)-1]
    last_part_of_title_page_link = splited_book_chapter_page_link[len(splited_book_title_page_link)-1]

    book_title_page_link_supplement = last_title_part_of_chapter_page_link[len(last_part_of_title_page_link):]

    return book_title_page_link_supplement


def get_book_title_link(book_link, book_title_page_length):
    splited_book_link = book_link.split('/')
    splited_book_title_link = splited_book_link[:book_title_page_length]
    book_title_link = '/'.join(splited_book_title_link)
    return book_title_link

