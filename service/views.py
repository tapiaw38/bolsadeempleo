from django.shortcuts import render
from service.models import Service
from service.forms import ServiceForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

# Create your views here.

'''
@login_required
def service_list(request):
    service = Service.objects.all().order_by('-created')
    contexto = {'service': service}
    return render (request, 'service/list_service.html', contexto)
'''
class ServiceList(LoginRequiredMixin, ListView):
    template_name = 'service/list_service.html'
    model = Service
    ordering = ('-created')
    paginate_by = 30
    context_object_name = 'service'

class ServiceDetail(LoginRequiredMixin, DetailView):
    template_name = 'service/detail.html'
    queryset = Service.objects.all()
    context_object_name = 'service'


class CreateService(LoginRequiredMixin, CreateView):

    template_name = 'service/new.html'
    form_class = ServiceForm
    success_url = reverse_lazy('list')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['person'] = self.request.user.person
        return context

@login_required
def category_search(request, search):
    if search:
        service = Service.objects.filter(category__contains=search)
    else:
        service = Service.objects.all()
    context = {'service':service}
    return render(request, 'service/search.html',context)


"""
@login_required
def create_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILE)
        if form.is_valid():
            form.save()
            return redirec(list)
        else:
            form = ServiceForm()
    contexto = {'user':request.user, 'form':form, 'person':request.user.person}
    return render(request, 'service/new.html')
"""