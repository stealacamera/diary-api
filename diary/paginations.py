from rest_framework.pagination import PageNumberPagination

class EntryPagination(PageNumberPagination):
    page_size = 25