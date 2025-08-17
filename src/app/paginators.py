from rest_framework.pagination import CursorPagination


class CustomCursorPaginator(CursorPagination):
    page_size = 6
    ordering = "id"
