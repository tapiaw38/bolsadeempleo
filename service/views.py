from django.shortcuts import render, redirect, get_object_or_404
from service.models import Service, Like
from service.forms import ServiceForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
import json
from django.http import HttpResponse
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib import messages
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

class DeleteService(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'service/service_delete.html'
    context_object_name = 'service'
    success_url = reverse_lazy('list') 


@login_required
def category_search(request, search):
    if search:
        service = Service.objects.filter(category__contains=search)
    else:
        service = Service.objects.all()
    context = {'service':service}
    return render(request, 'service/search.html',context)


@login_required
def like_service(request):
    user = request.user.person
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        service_obj = get_object_or_404(Service,id=service_id)

        if user in  service_obj.liked.all():
            service_obj.liked.remove(user)
        else:
            service_obj.liked.add(user)
        like, created_like = Like.objects.get_or_create(person=user,service_id=service_id)

        if not created_like:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value == 'Like'
        like.save()
        context={'likes_count':service_obj.num_likes, 'service_pk':service_obj.id}
    return HttpResponse(json.dumps(context), content_type='application/json')

    #return redirect('list')
@login_required
def delete_service(request):
    user = request.user.username
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        service_obj = Service.objects.get(id=service_id)
        service_obj.delete()
        context={'user':user, 'title':service_obj.title,}
    return HttpResponse(json.dumps(context), content_type='application/json')



def contact(request):
    if request.method == 'POST':
        subject = request.POST['asunto']
        msg = request.POST['msg']+' '+request.POST['email']
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['tapiaw38@gmail.com']
        send_mail(subject,msg,email_from,recipient_list)
        messages.success(request, "Mensaje enviado correctamente")
        return render(request,'service/contact.html')

    return render(request,'service/contact.html')



"""
        context={'likes_count':service_obj.num_likes}
    return HttpResponse(json.dumps(context), content_type='list')

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