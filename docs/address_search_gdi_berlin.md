# Address Search

### Important Links

- [GDI Berlin Viewer](https://gdi.berlin.de/viewer/main/)
- [Address WFS docs](https://gdi.berlin.de/data/adressen_berlin/docs/Datenformatbeschreibung_Adressen_Berlin.pdf)  (for query params)

## Overview
Address search requests are handled by `meinberlin/apps/geodata/wfs_client.py`

### Supported Search Patterns

- **Full addresses**: `"Hauptstraße 123"` → street + house number combination
- **Street names**: `"Hauptstraße"` → street name search
- **District names**: `"Mitte"` → district name search
- **House numbers**: `"25"` → exact house number match  
- **Postal codes**: `"10115"` → exact PLZ match


## Field Definitions

- `str_name`: Street name
- `hnr`: House number (Hausnummer)
- `plz`: Postal code (Postleitzahl)
- `bez_name`: District name (Bezirk)
- `ort_name`: Neighbourhood name (Ortsteil)

## API Reference

### `search_addresses(search_term: str, limit: int = 100, offset: int = 0) -> Dict`
Main search method 

**Parameters:**
- `search_term`: Address search string
- `limit`: Maximum number of results (default: 100)
- `offset`: Pagination offset (default: 0)

**Returns:** GeoJSON feature collection with address data

### `close()`
Clean up the HTTP session.

## Response Format

Returns GeoJSON feature collection with the following structure:

```json
{
  "features": [
    {
      "type": "Feature",
      "properties": {
        "str_name": "Hauptstraße",
        "hnr": "123",
        "plz": "10115",
        "bez_name": "Mitte",
        "ort_name": "Berlin-Mitte"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [13.12345, 52.54321]
      }
    }
  ],
  "total_count": 1
}
```


