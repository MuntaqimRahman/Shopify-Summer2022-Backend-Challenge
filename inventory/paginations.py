from rest_framework import pagination

SIZE_OF_PAGE=10
MAX_PAGE_SIZE=100


class PaginationConfig(pagination.PageNumberPagination):
    page_size = SIZE_OF_PAGE
    page_size_query_param = 'page_size'
    max_page_size = MAX_PAGE_SIZE
    page_query_param = 'page'