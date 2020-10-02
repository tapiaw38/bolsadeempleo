from django.shortcuts import render, redirect, get_object_or_404
from service.models import Service, Like, imageService
from service.forms import ServiceForm, ImageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, FormView
from django.urls import reverse_lazy
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib import messages
# Create your views here.
from datetime import datetime
from django.forms import modelformset_factory, formset_factory



def service_list(request):
    request_user = request.user.username
    services = Service.objects.all().order_by('-created')
    services = [list_serializer(service,request_user) for service in services]

    return HttpResponse(json.dumps(services), content_type='application/json')

def list_serializer(service,request_user):
    date = str(service.created)
    created = datetime.fromisoformat(date[:-13]).strftime('%d %B %Y %H:%M')

    return {

        'id':service.id,
        'user':service.user.username,
        'request_user':request_user,
        'picture':service.person.picture.url,
        'name':service.user.username,
        'picture_logo':[service.picture_logo],
        'category':service.category,
        'description':service.description,
        'direction':service.direction,
        'facebook_url':service.facebook_url,
        'liked':str(service.num_likes),
        'created':str(created),
        }

def service_index(request):
    request_user = request.user.username
    services = Service.objects.all().order_by("-created")[:4]
    services = [list_serializer2(service,request_user) for service in services]
    print(services)
    return HttpResponse(json.dumps(services), content_type='application/json')

def list_serializer2(service,request_user):
    date = str(service.created)
    created = datetime.fromisoformat(date[:-13]).strftime('%d %B %Y %H:%M')
    if service.picture_logo:
        picture = service.picture_logo.url
    else:
        picture = 0

    return {

        'id':service.id,
        'user':service.user.username,
        'request_user':request_user,
        'picture':service.person.picture.url,
        'name':service.user.username,
        'picture_logo': picture,
        'category':service.category,
        'description':service.description,
        'direction':service.direction,
        'facebook_url':service.facebook_url,
        'liked':str(service.num_likes),
        'created':str(created),
    }

class ServiceList(ListView):
    template_name = 'service/list_service.html'
    model = Service
    queryset = Service.objects.all().order_by("-created")[:60]
    #ordering = ('-created')
    paginate_by = 20
    context_object_name = 'service'

    """
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['service']=Service.objects.all().order_by("-created")[:5]
        return context
    """

class ServiceDetail(LoginRequiredMixin, DetailView):
    template_name = 'service/detail.html'
    queryset = Service.objects.all()
    context_object_name = 'service'

@login_required
def service_create(request):
    ImageFormset = modelformset_factory(
        imageService, 
        fields=('image',),
        labels= {'image':''},
        extra=1)
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            service = form.save(commit=False)
            service.user = request.user
            service.person = request.user.person
            service.save()

            for f in formset:
                try:
                    photo = imageService(service=service, image=f.cleaned_data['image'])
                    photo.save()

                except:
                    break
            return redirect('list')
            
    else:
        form = ServiceForm()
        formset = ImageFormset(queryset=imageService.objects.none())
    context = {
        'form':form,
        'formset':formset,
        'user': request.user,
        'person': request.user.person
    }
    return render(request, 'service/new.html', context)

def image_service(request):
    images = imageService.objects.all().order_by("-id")
    images = [images_serializer(image) for image in images]
    return HttpResponse(json.dumps(images), content_type='application/json')

def images_serializer(image):
    return {

        'id':image.id,
        'service':str(image.service.id),
        'image':image.image.url,

        }
'''
class CreateService(LoginRequiredMixin, FormView):
    template_name = 'service/new.html'
    form_class = ServiceForm
    second_form_class = formset_factory(ImageForm, extra=4)
    success_url = reverse_lazy('list')

    def get_context_data(self, **kwargs):

        context = super(CreateService,self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['person'] = self.request.user.person
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET) 

        return context

    def post(self,request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)

        if form.is_valid() and form2.is_valid():
            service = form.save(commit=False)
            service.image = form2.save()
            service.save()

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))
'''


class DeleteService(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'service/service_delete.html'
    context_object_name = 'service'
    success_url = reverse_lazy('list') 


@login_required
def category_search(request, search):
    if search:
        service = Service.objects.filter(category__contains=search).order_by("-created")
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
        context={'user':user, 'service_pk':service_obj.id}
        service_obj.delete()
        
        
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