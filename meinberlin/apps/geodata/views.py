from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .geosearch_client import GeoSearchClient
from .serializers import AddressSearchSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def search_addresses(request):
    """Search addresses in Berlin using WFS service with simple search parameter"""
    serializer = AddressSearchSerializer(data=request.query_params)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    validated_data = serializer.validated_data
    search_term = validated_data.get("search", "").strip()
    limit = validated_data.get("limit", 10)
    offset = validated_data.get("offset", 0)

    # Create cache key based on search parameters
    cache_key = f"address_search_{search_term}_{limit}_{offset}"

    # Try to get from cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        return Response(
            {
                "results": cached_result,
                "total_count": len(cached_result),
                "search_term": search_term,
                "pagination": {
                    "limit": limit,
                    "offset": offset,
                    "has_more": len(cached_result) == limit,
                },
            }
        )

    try:
        geosearch_client = GeoSearchClient()
        results = geosearch_client.search_addresses(query=search_term, limit=limit)

        # # Get total count for pagination (optional - might be expensive)
        # total_count = len(results)  # Default to current result count
        # if offset == 0:  # Only get total count on first page to avoid performance issues
        #     total_count = wfs_client.get_feature_count(search_term)

        # Cache results for 1 hour
        cache.set(cache_key, results, timeout=3600)

        return Response(
            {
                "results": results,
                "total_count": 100,
                "search_term": search_term,
                "pagination": {
                    "limit": limit,
                    "offset": offset,
                    "has_more": len(results) == limit and (offset + limit) < 100,
                },
            }
        )

    except Exception as e:
        return Response(
            {"error": str(e), "search_term": search_term},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
