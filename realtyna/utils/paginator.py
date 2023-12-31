from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size_query_param = "size"
    page_size = 10

    def get_paginated_response(self, data):
        return Response(
            {
                "success": True,
                "total": self.page.paginator.count,
                "page_size": self.get_page_size(self.request),
                "current_page": self.page.number,
                "last_page": self.page.paginator.num_pages,
                "data": data,
            }
        )
