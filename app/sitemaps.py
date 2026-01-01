from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5          # importance
    changefreq = 'monthly'  # frequency

    def items(self):
        # URL pattern names from urls.py
        return ['homepage', 'about', 'booking', 'round', 'round_booking']

    def location(self, item):
        return reverse(item)
