from django.views.generic import TemplateView

class TrackerView(TemplateView):

    template_name = "tracker.html"

class HomeView(TemplateView):

    template_name = "home.html"
