from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchlistPagination(PageNumberPagination): # the most common
    page_size = 7
    page_query_param = 'p'
    page_size_query_param = 'size'
    max_page_size = 10
    last_page_strings = 'end'
    
class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10
    offset_query_param = 'start'
    
class WatchListLCPagination(CursorPagination):
    page_size = 5
    ordering = 'created'
    cursor_query_param = 'record'