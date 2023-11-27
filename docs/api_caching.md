## Background

We have noticed that the page load of `mein.berlin.de/projekte/` is pretty slow with about 6s for 550 projects. Three API calls are particularly slow:

- https://mein.berlin.de/api/projects/?status=pastParticipation		2.811s
- https://mein.berlin.de/api/plans/					                      3.613s
- https://mein.berlin.de/api/extprojects/				                  5.041s

These paths correspond to the following api views:

- `projects/api.py::ProjectListViewSet`
- `plans/api.py::PlansListViewSet`
- `extprojects/api.py::ExternalProjectListViewSet`

we decided to start caching the endpoints with a redis backend.

## Developer Notes

The cache target is the `list` method of the following views:

- `ExternalProjectListViewSet`
- `PlansListViewSet`
- `ProjectContainerListViewSet`
- `ProjectListViewSet`
- `PrivateProjectListViewSet`

For adding cache keys we have added a new file `apps/contrib/api_caching.py` with functions for caching the list method of api views (see `cache_add_or_serialize`) and for caching querysets in general (see `cache_add_or_query`).

Cache keys expire after a timeout (default value 1h) or if a context specific signal is received (e.g. cache keys for projects are deleted if the signal for a saved project is detected).

The cache keys for projects are constracted by a hard-coded prefix (name-space) and a variable suffix. That is, the name of the cache key depends on the request query parameter `status` (e.g. `status=activeParticipation`). Cache keys are name-spaced so that 1) new status values can be added without breaking the cache, 2) we only need to know the name space to delete all keys related to projects, not each individual key.

The name space for each API endpoint is hard-coded and prefixed by a global caching prefix (see `contrib/api_caching.py::CACHE_KEY_PREFIX`). Typical cache keys look like this:
- `api_cache_projects`
- `api_cache_projects_activeParticipation`
- `api_cache_projects_pastParticipation`
- `api_cache_projects_futureParticipation`
- `api_cache_privateprojects`
- `api_cache_externalprojects`
- `api_cache_projectcontainers`
- `api_cache_plans`

If you want to delete all keys of a namespace use `cache.delete(namespace=..)`.

In production, we use Redis as cache backend (`django.core.cache.backends.redis.RedisCache`, see `settings/production.py::CACHES`). For development the cache backend is the default, that is local memory. If you want to enable it redis cache for local development, then copy the production settings to your `settings/local.py`.
ref: [django caching](https://docs.djangoproject.com/en/4.2/topics/cache/#local-memory-caching)
