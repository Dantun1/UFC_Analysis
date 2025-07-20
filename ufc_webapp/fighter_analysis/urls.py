from django.urls import path
from .views import HomeView, FightersView, SearchFighterView, FighterOverviewView, BlogView, EventsView, AboutView, \
    ModelsView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("fighters", FightersView.as_view(), name="fighters"),
    path("fighters/<int:pk>", FighterOverviewView.as_view(), name="fighter_overview"),
    path("search", SearchFighterView.as_view(), name="search"),
    path("blog", BlogView.as_view(), name="blog"),
    path("events", EventsView.as_view(), name="events"),
    path("about", AboutView.as_view(), name="about"),
    path("models", ModelsView.as_view(), name="models")
]