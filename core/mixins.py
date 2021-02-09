class ClientZoneMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_zone = self.request.GET.get('client_zone', '')
        context['client_zone'] = client_zone
        return context
