"""
>>> from django.core.paginator import Paginator
>>> from pagination.templatetags.pagination_tags import paginate
>>> from django.template import Template, Context

>>> p = Paginator(range(15), 2)
>>> pg = paginate({'paginator': p, 'page_obj': p.page(1)})
>>> pg['pages']
[1, 2, 3, 4, 5, 6, 7, 8]
>>> pg['records']['first']
1
>>> pg['records']['last']
2

>>> p = Paginator(range(15), 2)
>>> pg = paginate({'paginator': p, 'page_obj': p.page(8)})
>>> pg['pages']
[1, 2, 3, 4, 5, 6, 7, 8]
>>> pg['records']['first']
15
>>> pg['records']['last']
15

>>> p = Paginator(range(17), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(1)})['pages']
[1, 2, 3, 4, 5, 6, 7, 8, 9]

>>> p = Paginator(range(19), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(1)})['pages']
[1, 2, 3, 4, None, 7, 8, 9, 10]

>>> p = Paginator(range(21), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(1)})['pages']
[1, 2, 3, 4, None, 8, 9, 10, 11]

# Testing orphans
>>> p = Paginator(range(5), 2, 1)
>>> paginate({'paginator': p, 'page_obj': p.page(1)})['pages']
[1, 2]

>>> p = Paginator(range(21), 2, 1)
>>> pg = paginate({'paginator': p, 'page_obj': p.page(1)})
>>> pg['pages']
[1, 2, 3, 4, None, 7, 8, 9, 10]
>>> pg['records']['first']
1
>>> pg['records']['last']
2

>>> p = Paginator(range(21), 2, 1)
>>> pg = paginate({'paginator': p, 'page_obj': p.page(10)})
>>> pg['pages']
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> pg['records']['first']
19
>>> pg['records']['last']
21

>>> t = Template("{% load pagination_tags %}{% autopaginate var 2 %}{% paginate %}")

>>> from django.http import HttpRequest as DjangoHttpRequest
>>> class HttpRequest(DjangoHttpRequest):
...     page = 1

>>> t.render(Context({'var': range(21), 'request': HttpRequest()}))
u'\\n\\n<div class="pagination">...
>>>
>>> t = Template("{% load pagination_tags %}{% autopaginate var %}{% paginate %}")
>>> t.render(Context({'var': range(21), 'request': HttpRequest()}))
u'\\n\\n<div class="pagination">...
>>> t = Template("{% load pagination_tags %}{% autopaginate var 20 %}{% paginate %}")
>>> t.render(Context({'var': range(21), 'request': HttpRequest()}))
u'\\n\\n<div class="pagination">...
>>> t = Template("{% load pagination_tags %}{% autopaginate var by %}{% paginate %}")
>>> t.render(Context({'var': range(21), 'by': 20, 'request': HttpRequest()}))
u'\\n\\n<div class="pagination">...
>>> t = Template("{% load pagination_tags %}{% autopaginate var by as foo %}{{ foo }}")
>>> t.render(Context({'var': range(21), 'by': 20, 'request': HttpRequest()}))
u'[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]'

"""
