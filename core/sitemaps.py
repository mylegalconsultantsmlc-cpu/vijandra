from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Service, Blog

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'
    def items(self):
        return ['home','all_services','contact_us','about_us','terms_and_conditions','privacy_policy','blog_list']
    def location(self, item):
        return reverse(item)

class ServiceSitemap(Sitemap):
    changefreq = 'monthly'
    def items(self):
        return Service.objects.filter(published=True)

class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    def items(self):
        return Blog.objects.filter(published=True)
