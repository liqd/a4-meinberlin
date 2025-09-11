import requests
from urllib.parse import quote
import json
from typing import List, Dict, Optional

class WFSClient:
    BASE_URL = "https://gdi.berlin.de/services/wfs/adressen_berlin"
    
    def __init__(self):
        self.session = requests.Session()
    
    def build_search_filter(self, search_term: str) -> str:
        """Build CQL filter for the search term"""
        if not search_term or not search_term.strip():
            return ""
        
        search_term = search_term.strip()
        
        conditions = [
            f"str_name LIKE '%{search_term}%'",
            f"hausnummer = '{search_term}'",
            f"plz = '{search_term}'", 
            f"bezirk LIKE '%{search_term}%'",
            f"ortsteil LIKE '%{search_term}%'"
        ]
        
        return f"({' OR '.join(conditions)})"
    
    def search_addresses(self, search_term: str, limit: int = 100, offset: int = 0) -> Dict:
        """Search features using CQL filter"""
        try:
            base_params = {
                'service': 'WFS',
                'version': '2.0.0',
                'request': 'GetFeature',
                'typeNames': 'adressen_berlin:adressen_berlin',
                'outputFormat': 'application/json',
                'srsName': 'EPSG:4326',
                'count': str(limit),
                'startIndex': str(offset)
            }
            
            if search_term:
                cql_filter = self.build_search_filter(search_term)
                if cql_filter:
                    base_params['CQL_FILTER'] = cql_filter
            

            response = self.session.get(self.BASE_URL, params=base_params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Error searching features: {e}")
            return {"results": [], "total_count": 0}
    
    def get_feature_count(self, search_term: str = None) -> int:
        """Get total count of features matching the search using CQL filter"""
        try:
            base_params = {
                'service': 'WFS',
                'version': '2.0.0',
                'request': 'GetFeature',
                'typeNames': 'adressen_berlin:adressen_berlin',
                'outputFormat': 'application/json',
                'srsName': 'EPSG:4326',
                'maxFeatures': '0'  # No features, just count
            }
            
            if search_term:
                cql_filter = self.build_search_filter(search_term)
                if cql_filter:
                    base_params['CQL_FILTER'] = cql_filter
            
            response = self.session.get(self.BASE_URL, params=base_params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get('total_count', 0)
            
        except Exception as e:
            print(f"Error getting feature count: {e}")
            return 0
    
    def close(self):
        self.session.close()
