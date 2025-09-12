from typing import Dict
from typing import Optional

import requests


class GeoSearchClient:
    BASE_URL = "https://gdi.berlin.de/searches/bkg/geosearch"
    DEFAULT_BBOX = (
        "13.088,52.338,13.761,52.675"  # Berlin bounding box in EPSG:4326 (WGS84)
    )
    DEFAULT_SRS = "EPSG:4326"

    def __init__(self):
        self.session = requests.Session()

    def search_addresses(
        self, query: str, limit: int = 100, bbox: Optional[str] = None
    ) -> Dict:
        """
        Search addresses using the dedicated geosearch endpoint

        Args:
            query: Address search query (e.g., "Reuterstraße 5, 12053 Berlin - Neukölln")
            limit: Maximum number of results to return
            bbox: Bounding box in format "minx,miny,maxx,maxy" (EPSG:25833)
                   Defaults to Berlin area if not specified

        Returns:
            Dictionary with search results
        """
        try:
            params = {
                "bbox": self.DEFAULT_BBOX,
                "outputformat": "json",
                "srsName": self.DEFAULT_SRS,
                "count": str(limit),
                "query": query,
            }

            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()

            return response.json()

        except Exception as e:
            print(f"Search error: {e}")
            return {"results": [], "total_count": 0}

    def close(self):
        """Close the session"""
        self.session.close()
