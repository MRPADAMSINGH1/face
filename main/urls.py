from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("newsletter", views.newsletter, name="newsletter"),
    path("Our Teams", views.ourteam, name="Our Teams"),
    path("About", views.about, name="About"),
     path("Contact", views.contact, name="contact"),

]