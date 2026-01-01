from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        # உங்கள் app URLs இல் "name=" கொடுத்தவை
        return ['homepage', 'round', 'login']  

    def location(self, item):
        return reverse(item)
