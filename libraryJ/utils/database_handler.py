from ..models import Website
from ..models import Book

def find_website_by_domain(website_domain):
    try:
        name = website_domain.split('.')
        website = Website.objects.get(name=name[1])
        return website
    except Website.DoesNotExist:
        return None
