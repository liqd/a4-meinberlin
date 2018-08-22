from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class RootSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return ["wagtail_sitemap", "adhocracy4_sitemap"]

    def location(self, obj):
        return reverse(obj)
