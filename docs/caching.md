

## Background

We have noticed that the page load of `mein.berlin.de/projekte/` is pretty slow with about 6s for 550 projects. Three API calls are particularly slow:

- https://mein.berlin.de/api/projects/?status=pastParticipation		2.811s
- https://mein.berlin.de/api/plans/					                      3.613s
- https://mein.berlin.de/api/extprojects/				                  5.041s

These urls correspond to the following api views:

- `projects/api.py::ProjectListViewSet`
- `plans/api.py::PlansListViewSet`
- `extprojects/api.py::ExternalProjectListViewSet`

Since we were not able to improve the serializers for these views (see `docs/performance_of_plans_serializer.md`) we decided to start caching the endpoints with a redis backend.

## Developer Notes

The cache target is the `list` method of the following views:

- `ExternalProjectViewSet`
- `PlansViewSet`
- `ProjectContainerViewSet`
- `ProjectViewSet`
- `PrivateProjectViewSet`

To avoid repeating code for adding cache keys we have added a new file `apps/contrib/caching.py` with functions for caching the list method of api views (see `cache_add_or_serialize`) and for caching query sets in general (see `cache_add_or_query`).

Cache keys expire after a timeout (default value 1h) or if a context specific signal is received (e.g. cache keys for projects are deleted if the signal for a saved project is detected).

The cache keys for projects are dynamic. That is, the cache value depends on the request query parameter `status` (e.g. `status=activeParticipation`). The status value is used as a suffix in the key generation. Cache keys are name-spaced so that 1) new status values can be added without breaking the cache, 2) we only need to know the name space to delete all keys related to projects, not each individual key.

The name space for each API endpoint is hard-coded and prefixed by a global caching prefix (see `contrib/caching.py::CACHE_KEY_PREFIX`). Typical cache keys look like this:
- `api_cache_projects`
- `api_cache_projects_activeParticipation`
- `api_cache_projects_pastParticipation`
- `api_cache_projects_futureParticipation`
- `api_cache_privateprojects`
- `api_cache_externalprojects`
- `api_cache_projectcontainers`
- `api_cache_plans`

In production, we use redis as cache backend (`django_redis.cache.RedisCache`, see `settings/production.py::CACHES`). For development the cache backend is disabled (see `settings/base.py::CACHES`). If you want to enable it locally, then copy the production settings to your `settings/local.py`.

Some more notes about the caching module:
- it is indented to be imported as a module instead of importing individual methods so that you call `caching.add_or_query(..)` instead of `add_or_query(..)`, for example
- `caching.delete(..)` can either be given a namespace or an explicit list of keys to be deleted and returns all keys that were deleted
