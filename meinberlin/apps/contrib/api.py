from typing import Any
from typing import Dict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from meinberlin.apps.contrib.templatetags.contrib_tags import (
    get_proper_elided_page_range,
)


class APIPagination(PageNumberPagination):
    """PageNumberPagination which adds additional data to the response.

    Adds the following extra data:
        page_size: size of the page
        page_count: number of overall pages
        page_elided_range: elided page range
    """

    page_size = 15
    # Allow fetching of all items for the map view
    page_size_query_param = "page_size"

    def get_paginated_response(self, data: Dict[str, Any]) -> Response:
        response = super(APIPagination, self).get_paginated_response(data)
        response.data["page_size"] = self.page_size
        response.data["page_count"] = self.page.paginator.num_pages
        response.data["page_elided_range"] = get_proper_elided_page_range(
            self.page.paginator, self.page.number
        )
        return response
