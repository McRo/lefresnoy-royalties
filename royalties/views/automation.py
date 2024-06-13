from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class SendNotificationToArtist(LoginRequiredMixin, TemplateView):
    template_name = 'notification/list.html'
    
