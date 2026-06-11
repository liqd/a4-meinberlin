# BPLAN Project API

mein.berlin provides an external REST API to create and manage BPLAN projects.

## Background

Bplans define binding regulations for urban planning, specifying land
use (e.g. housing, offices, green spaces) and building parameters like height
and footprint. Citizens can participate in the process and provide feedback
on the plans. As the central participation platform of the city of Berlin, we want
to show all Bplans which allow participation in our project overview. The digital participation itself is
provided by the Diplan platform. Bplans are mostly created via this api but they can also be added by initiators from the dashboard.

### Integration with Diplan

Diplan manages Bplans and provides the participation feature. The only functionality in meinBerlin is to display
Bplans in the project overview and link out to Diplan.

#### Key behaviours:

- The `district` is provided as a short code string by Diplan, and corresponds to an "Administrative District" record created in the admin
- The Bplan location is provided by Diplan
- Participation (statements) happens directly on Diplan; meinBerlin does not collect statements
- Bplans are shown until unpublished via this api

## Prerequisites

To use this API you need to have received an email and a password for the
API user and the `id` of your organisation.

## Authentication

The API supports the HTTP Basic Authentication mechanism and requires a TLS connection to prevent
leaking the login credentials. You need the email and password combination from your user account as mentioned in the
Prerequisites above.

## Endpoints

* [Create Bplan](#Creating-a-Bplan) : `POST https://mein.berlin.de/api/organisations/<organisation-id>/bplan/`
* [Update Bplan](#Updating-a-Bplan) : `PATCH /https://mein.berlin.de/api/organisations/<organisation-id>/bplan/<bplan-id>/`

## Creating a Bplan

Create a new Bplan within the organisation designated by `organisation-id`.

**URL** : `https://mein.berlin.de/api/organisations/<organisation-id>/bplan/`

**Method** : `POST`

**Parameters** : `organisation-id`: Integer - id of the organisation the bplan will be added to

**Auth required** : YES

**Permissions required** : User account must be initiator for the specified organisation

**Data constraints**

The following fields need to be provided:

- *name*: string
  - Name of the BPLAN (e.g. used as the title of the project tile)
  - Maximum length of 120 chars, however longer input is accepted and will be cut to 120
- *administrative_district*: string
  - District short code, corresponding to an Administrative District created in the meinBerlin admin, eg `mi` for `Mitte`
  - See the [complete district codes table](#district-codes-table) for reference.
  - Maximum length of 120 chars
- *description*: string
  - Description of the BPLAN shown in the project tile
  - Maximum length of 250 chars, however longer input is accepted and will be cut to 250
- *url*: string
  - URL of the external site the BPLAN is embedded on
- *office_worker_email*: string
  - Email of the office worker to receive notifications about changes
- *is_draft*: bool
  - Whether the plan is still a draft or should be published
- *start_date*: string
  - Start date of the participation
  - [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601)
    (if no time zone is defined, german time zones UTC+01 and UTC+02 are used)
- *end_date*: string
  - End date of the participation in
  - [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601)
    (if no time zone is defined, german time zones UTC+01 and UTC+02 are used)
- *point*: string containing valid geojson
  - Location of the bplan
  - Projection: WGS84 / EPSG:4326
- *tile_image*: string (optional)
  - Base64 encoded image
  - Minimal resolution 500x300 px (width x height)
  - Maximum file size 10MB
  - Allowed formats: png, jpeg, gif
  - If not provided, the placeholder image will be automatically used in the frontend
- *image_copyright*: string
  - Copyright shown for the image
  - Maximum length of 120 chars
- *image_alt_text*: string
  - Alt text for the tile image
  - Maximum length of 80 chars

#### Data example

```json
{
  "name": "Luisenblock Ost - Bebauungsplan 1-70",
  "administrative_district": "mi",
  "description": "Der Luisenblock Ost soll städtebaulich neu geordnet werden. Nutzungen des Deutschen Bundestages sollen in einem Sondergebiet als Auftakt des 'Band des Bundes' zusammengefasst werden.",
  "url": "https://berlin.de/ba-marzahn-hellersdorf/.../bebauungsplan.649020.php",
  "is_draft": false,
  "start_date": "2017-01-01T00:00",
  "end_date": "2018-01-01T00:00",
  "point": {
    "type": "Feature",
    "geometry": {
      "type": "Point",
      "coordinates": [
        13.411924777644563,
        52.499598134440944
      ]
    }
  },
  "image_copyright": "BA Marzahn-Hellersdorf"
}
```

### Success Response

**Condition** : If all data is valid

**Code** : `201 CREATED`

**Response**

- id: Integer
  - The id of the newly created bplan. Required to make modifications to this bplan.

**Content example**

```json
{
  "id": 1
}
```

### Error Responses

**Condition** : Invalid data (e.g. missing field).

**Code** : `400 Bad Request`

**Content example**

```json
{
  "name": [
    "This field is required."
  ]
}
```

## Testing

Note: user should be sent as email address, not username.

### Example for `curl`

```bash
curl \
 -X POST https://mein.berlin.de/api/organisations/5/bplan/ \
 --user 'test@example.com':'password' \
 -H "Content-Type: application/json" \
 -d \
 '
 {
   "name":"Luisenblock Ost - Bebauungsplan 1-70",
   "administrative_district": "mi",
   "description": "Test",
   "url": "https://mein.berlin.de",
   "office_worker_email": "test@example.com",
   "start_date": "2019-01-01T00:00",
   "end_date": "2022-01-01T00:00",
   "point": "{\"type\": \"Feature\",\"geometry\": {\"type\": \"Point\", \"coordinates\":[13.411924777644563,52.499598134440944]}}"
 }
'
```

### Example for `curl` and local testing

```bash
curl  -X POST http://127.0.0.1:8003/api/organisations/1/bplan/ \
 --user 'admin@liqd.net':'password' \
 -H "Content-Type: application/json" \
 -d \
 '
 {
   "name":"Luisenblock Ost - Bebauungsplan 1-70",
    "administrative_district": "mi",
   "description": "Test",
   "url": "https://mein.berlin.de",
   "office_worker_email": "test@example.com",
   "start_date": "2019-01-01T00:00",
   "end_date": "2022-01-01T00:00",
   "point": "{\"type\": \"Feature\",\"geometry\": {\"type\": \"Point\", \"coordinates\":[13.411924777644563,52.499598134440944]}}"
 }
'
```

## Updating a Bplan

Update an existing Bplan with the id `bplan-id` within the organisation designated by`organisation-id`.

**URL** : `https://mein.berlin.de/api/organisations/<organisation-id>/bplan/<bplan-id>/`

**Method** : `PATCH`

**Parameters** :

- `organisation-id`: Integer
  - id of the organisation the bplan will be added to
- `bplan-id`: Integer
  - id of the bplan to update

**Auth required** : YES

**Permissions required** : User account must be initiator for the specified organisation

**Data constraints**

See [data example](#data-example) above

### Success Response

**Condition** : If all data is valid

**Code** : `200 OK`

**Response**

- id: Integer
  - The id of the newly created bplan. Required to make modifications to this bplan.

**Content example**

```json
{
  "id": 1
}
```

### Error Responses

**Condition** : Invalid data (e.g. missing field).

**Code** : `400 Bad Request`

**Content example**

```json
{
  "name": [
    "Not a valid string"
  ]
}
```

## Testing

### Example for `curl`

```bash
curl \
 -X PATCH https://mein.berlin.de/api/organisations/5/bplan/1 \
 --user 'test@example.com':'password' \
 -H "Content-Type: application/json" \
 -d \
'
 {
   "is_draft": true
 }
'
```

### Example for `curl` and local testing

```bash
curl  -X PATCH http://127.0.0.1:8003/api/organisations/1/bplan/16/ \
 --user 'admin@liqd.net':'password' \
 -H "Content-Type: application/json" \
 -d \
'
 {
   "is_draft": true
 }
'
```

## Email notifications

Creating or updating a Bplan triggers automated emails. The table below lists
what is sent, to whom, and when.

| Email | Trigger | Recipients | Links to |
|-------|---------|------------|----------|
| Office worker confirmation | Bplan created or updated | `office_worker_email` | Body: the Bplan's Diplan `url`. CTA button: the meinBerlin project overview (Kiezradar) |
| New project notification | Bplan created | All *other* initiators of the organisation (the creating API user is excluded) | The Bplan's Diplan `url` |
| Search profile match | Bplan published | Users whose saved search profile matches the Bplan | The Bplan's Diplan `url` |

Notes:

- The office worker confirmation is sent on creation and on content changes,
  but **not** when only the map location (`point`) is fetched or when the Bplan
  is archived.
- Recipients of the "new project" and "search profile match" emails can opt out
  via their notification settings.

# Berlin Districts Reference

Added/edited using the admin.

| District | Short Code |
|----------|------------|
| Mitte | mi |
| Friedrichshain-Kreuzberg | fk |
| Pankow | pa |
| Charlottenburg-Wilmersdorf | cw |
| Spandau | sp |
| Steglitz-Zehlendorf | sz |
| Tempelhof-Schöneberg | ts |
| Neukölln | nk |
| Treptow-Köpenick | tk |
| Marzahn-Hellersdorf | mh |
| Lichtenberg | li |
| Reinickendorf | rd |
| Gesamtstädtisch | be |