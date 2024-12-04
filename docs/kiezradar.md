## Kiezradar module
Allows the selection of filters to be saved as a search profile. A user can have several search profiles.

### Structure
meinberlin/apps/kiezradar  
models.py:  
- A Kiezradar query with a text field which can accommodate free text query.
- A search profile related to user, corresponds to the project overview filters, and provides multiselect options through m2m relations with the existing project overview filters. The idea is that these filters can be attached to different Search Profiles.  

serializers.py  
- A Serializer with a custom create() and update() for creating/updating m2m relations of the SearchProfile.

api.py  
ModelViewset for API create and update requests


