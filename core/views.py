from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Page d'accueil"""
    template_name = 'core/home.html'


class ServicesView(TemplateView):
    """Page des services"""
    template_name = 'core/services.html'


class AboutView(TemplateView):
    """Page à propos"""
    template_name = 'core/about.html'


class PrivacyPolicyView(TemplateView):
    """Page politique de confidentialité"""
    template_name = 'core/privacy.html'


class TermsView(TemplateView):
    """Page conditions d'utilisation"""
    template_name = 'core/terms.html'
