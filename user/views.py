from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from user.models import Person
from user.forms import PersonForm
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DetailView, FormView
from django.db.utils import IntegrityError
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views


from service.models import Service
# Create your views here.


class index(TemplateView):
    template_name = 'user/index.html'


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'user/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user =  self.get_object()
        context['services'] = Service.objects.filter(user=user).order_by('-created')
        return context
    

def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)
        if user:
            login(request, user)
            return redirect('list')
        else:
            messages.error(request, "El usuario o contraseña son invalidos")
            return render(request,'user/log_in.html')
    return render(request,'user/log_in.html')

def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']
        
        # Validate password!
        if  password != password_confirmation:
            messages.error(request, "Las contraseñas ingresadas no coinciden")
            return render(request, 'user/sign_up.html')
        if len(password) < 7 or len(password_confirmation) < 7:
            messages.error(request, "La contraseña debe tener 8 o más caracteres")
            return render(request, 'user/sign_up.html')
        # Validate User!
        for i in username:
            if i == " ":
                messages.error(request, "El nombre de usuario no puede tener espacios en blanco")
                return render(request, 'user/sign_up.html')
        try:      
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            messages.error(request, "Este nombre de usuario ya esta en uso, por favor elige otro")
            return render(request, 'user/sign_up.html')
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()

        person = Person(user=user)
        person.save()
        
        return render(request,'user/log_in.html')

    return render(request,'user/sign_up.html')

@login_required
def update_person(request):

    person = request.user.person

    if  request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            person.picture = data['picture']
            person.phone_number = data['phone_number']
            person.direction = data['direction']
            
            person.save()
            url = reverse('detail', kwargs={'username':request.user.username})
            return redirect(url)
    else:
        form = PersonForm()
    contexto={'person':person,'user':request.user,'form':form}
    return render(request,'user/update_person.html',contexto)

@login_required
def log_out(request):
    logout(request)
    return redirect('index')



