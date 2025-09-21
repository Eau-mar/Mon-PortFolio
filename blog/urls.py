from django.urls import path
from .import views
from .models import Projet
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView


class ProjetSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Projet.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at
    
sitemaps = {'projet' : ProjetSitemap}

urlpatterns = [
    path('sitemap.xml', sitemap,
         {'sitemaps' : sitemaps},
         name = 'django.contrib.sitemaps.views.sitemap'
         ),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    path('', views.index, name='home'),
    path('portfolio/', views.portfolio, name="portfolio"),
    path('portfolio/<slug:slug>/plus', views.plus, name='plus'),
    path('confident/', views.confident, name='confident'),
    path("ajouter-temoignage/", views.ajouter_temoignage, name="ajouter_temoignage"),
    path("envoyer-message/", views.envoyer_message, name="envoyer_message"),
    path('envoyer-devis/', views.envoyer_devis, name='envoyer_devis'),
]

handler404 = "blog.views.client_page_not_found"

