from typing import Dict

import requests


class WFSClient:
    BASE_URL = "https://gdi.berlin.de/services/wfs/adressen_berlin"

    def __init__(self):
        self.session = requests.Session()

    def build_search_filter(self, search_term: str) -> str:
        """Build CQL filter for the search term"""
        if not search_term or not search_term.strip():
            return ""

        search_term = search_term.strip()

        filters = []

        # Text search fields (case insensitive if supported)
        text_fields = ["str_name", "bez_name"]
        for field in text_fields:
            filters.append(f"{field} LIKE '%{search_term}%'")

        # Exact match for numeric fields
        if search_term.isdigit():
            # hnr = hausnummer
            numeric_fields = ["hnr", "plz"]
            for field in numeric_fields:
                print("appending some fucking shit")
                filters.append(f"{field} = '{search_term}'")

        if not filters:
            return ""

        return " OR ".join([f"({f})" for f in filters])

    def search_addresses(
        self, search_term: str, limit: int = 100, offset: int = 0
    ) -> Dict:
        """Multi-phase search for better results"""
        if not search_term or not search_term.strip():
            return {"features": [], "total_count": 0}

        search_term = search_term.strip()

        # Phase 1: Try exact matches first
        exact_results = self._search_exact(search_term, limit)
        if exact_results.get("features"):
            return exact_results

        # Phase 2: Try smart pattern matching
        pattern_results = self._search_pattern(search_term, limit)
        if pattern_results.get("features"):
            return pattern_results

        # Phase 3: Fallback to broad search
        return self._search_broad(search_term, limit, offset)

    def _search_exact(self, search_term: str, limit: int) -> Dict:
        """Search for exact matches"""
        filters = []

        if search_term.isdigit():
            if len(search_term) == 5:
                filters.append(f"plz = '{search_term}'")
            else:
                filters.append(f"hnr = '{search_term}'")
        else:
            filters.append(f"str_name = '{search_term}'")
            filters.append(f"bez_name = '{search_term}'")
            filters.append(f"ort_name = '{search_term}'")

        return self._execute_search(" OR ".join(filters), limit)

    def _search_pattern(self, search_term: str, limit: int) -> Dict:
        """Search with pattern recognition"""
        # Try to detect address patterns
        parts = search_term.split()

        if len(parts) >= 2 and parts[-1].isdigit():
            # Pattern: "Streetname 123"
            street = " ".join(parts[:-1])
            number = parts[-1]
            filter_str = f"str_name LIKE '%{street}%' AND hnr = '{number}'"
            return self._execute_search(filter_str, limit)

        # Default to street name search
        return self._execute_search(f"str_name LIKE '%{search_term}%'", limit)

    def _search_broad(self, search_term: str, limit: int, offset: int) -> Dict:
        """Broad search as fallback"""
        filters = [
            f"str_name LIKE '%{search_term}%'",
            f"bez_name LIKE '%{search_term}%'",
            f"ort_name LIKE '%{search_term}%'",
        ]

        if search_term.isdigit():
            filters.append(f"hnr = '{search_term}'")
            filters.append(f"plz = '{search_term}'")

        return self._execute_search(" OR ".join(filters), limit, offset)

    def _execute_search(self, cql_filter: str, limit: int, offset: int = 0) -> Dict:
        """Execute the actual search"""
        try:
            params = {
                "service": "WFS",
                "version": "2.0.0",
                "request": "GetFeature",
                "typeNames": "adressen_berlin:adressen_berlin",
                "outputFormat": "application/json",
                "srsName": "EPSG:4326",
                "count": str(limit),
                "startIndex": str(offset),
                "CQL_FILTER": cql_filter,
            }

            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            print(f"Search error: {e}")
            return {"features": [], "total_count": 0}

    def close(self):
        """Close the session"""
        self.session.close()
