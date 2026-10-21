from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("login/", views.DashboardLoginView.as_view(), name="login"),
    path("logout/", views.DashboardLogoutView.as_view(), name="logout"),
    path("", views.home, name="home"),

    path("leads/", views.leads_list, name="leads_list"),
    path("leads/<int:pk>/", views.lead_detail, name="lead_detail"),

    path("blog/", views.blog_list, name="blog_list"),
    path("blog/new/", views.blog_form, name="blog_add"),
    path("blog/<int:pk>/edit/", views.blog_form, name="blog_edit"),
    path("blog/<int:pk>/delete/", views.blog_delete, name="blog_delete"),

    path("testimonials/", views.testimonial_list, name="testimonial_list"),
    path("testimonials/new/", views.testimonial_form, name="testimonial_add"),
    path("testimonials/<int:pk>/edit/", views.testimonial_form, name="testimonial_edit"),
    path("testimonials/<int:pk>/delete/", views.testimonial_delete, name="testimonial_delete"),

    path("portfolio/", views.portfolio_list, name="portfolio_list"),
    path("portfolio/new/", views.portfolio_form, name="portfolio_add"),
    path("portfolio/<int:pk>/edit/", views.portfolio_form, name="portfolio_edit"),
    path("portfolio/<int:pk>/delete/", views.portfolio_delete, name="portfolio_delete"),
]
