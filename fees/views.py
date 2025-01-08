from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView
from .models import Fee


class FeeListView(ListView):
    model = Fee
    template_name = 'fees/list.html'
    context_object_name = 'fees'


class FeeUpdateView(UpdateView):
    model = Fee
    fields = ['min_investment', 'max_investment', 'fee_percentage']
    template_name = 'fees/update.html'
    context_object_name = 'fee'
    success_url = reverse_lazy('fee_list')

    def get_object(self):
        # You can customize how to get the object (user) if needed.
        return Fee.objects.get(id=self.kwargs['pk'])