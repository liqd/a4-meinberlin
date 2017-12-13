# BPLAN Project API

mein.berlin provides an external REST API to create and manage BPLAN projects.

## Prerequisites

To use this API you need to have received the *email* and *password* for the
API user and the *id* of your organisation.

## Authentication

The API supports the HTTP Basic Authentication mechanism using your *email* and *password*.

## Ceating a BPLAN

The following data fields are posted as JSON to create and publish a BPLAN
project:

-   *name*: Name of the BPLAN (e.g. used as the title of the project tile)
-   *description*: Description of the BPLAN shown in the project tile
-   *url*: URL of the external site the BPLAN is embedded on
-   *office_worker_email*: Email of the office worker to receive the statement emails
-   *start_date*: Start date of the participation [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601) (if no time zone is  defined,german time zones UTC+1 and UTC+2 are used)
-   *end_date*: End date of the participation in [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601) (if no time zone is  defined,  german time zones UTC+1 and UTC+2 are used)
-   *image_url*: URL of the image that is used in the project tile
-   *image_copyright*: Copyright shown for the image

API endpoint for POST requests:

    https://mein.berlin.de/api/organisations/<organisation-id>/bplan/

The response will contain the following fields:

-   *id*: The id of the BPLAN to be used for updates
-   *embed_code*: The `<iframe>` to embed the created BPLAN project

Example:

    data = {
        "name":"Luisenblock Ost - Bebauungsplan 1-70",
        "description": "Der Luisenblock Ost soll städtebaulich neu geordnet werden. Nutzungen des Deutschen Bundestages sollen in einem Sondergebiet als Auftakt des 'Band des Bundes' zusammengefasst werden.",
        "url": "https://berlin.de/ba-marzahn-hellersdorf/.../bebauungsplan.649020.php",
        "office_worker_email": "test@example.com",
        "start_date": "2017-01-01T00:00",
        "end_date": "2018-01-01T00:00",
        "image_url": "http://berlin.de/images/.../bebauungsplan.649020.png",
        "image_copyright": "BA Marzahn-Hellersdorf",
    }
    res = POST(https://mein.berlin.de/api/organisations/5/bplan/, data)
    print(res)
    {
        "id":36,
        "embed_code":
            "<iframe
                height="500"
                style="width: 100%; min-height: 300px; max-height: 100vh"
                src="https://mein.berlin.de/embed/projects/luisenblock-ost-bebauungsplan-1-70/"
                frameborder="0">
            </iframe>"
    }

The participation will start end end automatically at the scheduled time.

## Updating a BPLAN Project

To update a BPLAN setting send a PATCH request with the field to update using
the *id* of the BPLAN from the create response.

API endpoint for PATCH:

    https://mein.berlin.de/api/organisations/<organisation-id>/bplan/<bplan-id>/

Example:

    data = {
        "end_date": "2019-01-01T00:00",
    }
    res = PATCH(https://mein.berlin.de/api/organisations/5/bplan/36/, data)

## Publishing/Unpublishing a BPLAN Project

When creating a BPLAN project as above, the project is immediately being
published. To create a BPLAN project in a draft state set the *is_draft*
parameter:

    data = {
        ...
        "is_draft": True,
    }
    res = POST(https://mein.berlin.de/api/organisations/5/bplan/, data)

To change the draft state, update the BPLAN project via PATCH.

Publish:

    data = {
        "is_daft": False
    }
    res = PATCH(https://mein.berlin.de/api/organisations/5/bplan/36/, data)

Unpublish:

    data = {
        "is_daft": True
    }
    res = PATCH(https://mein.berlin.de/api/organisations/5/bplan/36/, data)
