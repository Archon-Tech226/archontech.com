from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("about/", views.about, name="about"),
    path("team/", views.team, name="team"),
    path("contact/", views.contact, name="contact"),
    path("behind-the-build/", views.blog, name="blog"),
    path("behind-the-build/<slug:slug>/", views.blog_post, name="blog_post"),
]
