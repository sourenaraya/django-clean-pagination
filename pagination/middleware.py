import re

from django.conf import settings


URL_PATTERN = getattr(
    settings, 
    'PAGINATION_URL_PATTERN', 
    r'(page/)(?P<page>\d+)/$'
)
CLEAN_URL = getattr(settings, 'PAGINATION_CLEAN_URL', False)


def get_page(self):
    """
    A function which will be monkeypatched onto the request to get the current
    integer representing the current page.
    """
    try:
        return int(self.REQUEST['page'])
    except (KeyError, ValueError, TypeError):
        return 1


class PaginationMiddleware(object):
    """
    Inserts a variable representing the current page onto the request object if
    it exists in either **GET** or **POST** portions of the request.
    """
    def __init__(self):
        self.path = re.match(r'\(([\w/_\.]+)\)', URL_PATTERN).group(1)
        self.pattern = re.compile(URL_PATTERN)

    def process_request(self, request):

        if CLEAN_URL:
            current_page = 1
            separator = ''
            page_path = self.path
            if page_path == '/':
                page_path = ''
                separator = '/'
            match = self.pattern.search(request.path)
            if match:
                current_page = int(match.group('page'))
                path = re.sub(URL_PATTERN, separator, request.path)
                del request.path_info
                request.__class__.path_info = path

            request.__class__.page = current_page
            request.__class__.page_path = page_path
        else:
            request.__class__.page = property(get_page)
