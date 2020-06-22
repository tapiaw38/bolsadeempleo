from django.shortcuts import render
from service.models import Service
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def service_list(request):
    service = Service.objects.all().order_by()
    contexto = {'service': service}
    return render (request, 'service/list_service.html', contexto)

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