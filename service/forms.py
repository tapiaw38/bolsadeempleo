from django import forms
from service.models import Service, Message


class ServiceForm(forms.ModelForm):

    class Meta:

        model = Service

        fields = (
            'user', 
            'person', 
            'title', 
            'category', 
            'description', 
            'direction', 
            'facebook_url', 
            'picture_logo'
            )
        
        CATEGORY_CHOICES = [
            ('Compras y Shopping', 'Compras y Shopping'),
            ('Informática y Electrónica','Informática y Electrónica'),
            ('Construcción y Contratistas','Construcción y Contratistas'),
            ('Deportes y Recreacción','Deportes y Recreacción'),
            ('Educación','Educación'),
            ('Hogar y Jardin','Hogar y Jardin'),
            ('Industria y Agricultura','Industria y Agricultura'),
            ('Medios de Comunicación','Medios de Comunicación'),
            ('Servicios Profecionales','Servicios Profecionales'),
            ('Ropa y Accesorios','Ropa y Accesorios'),
            ('Salud y Medicina','Salud y Medicina'),
            ('Servicios Legales y Financieros','Servicios Legales y Financieros'),
            ('Viajes y Trasportes','Viajes y Trasportes'),
            ('Gastronomia','Gastronomia'),
        ]



        widgets = {
            'category':forms.Select(choices=CATEGORY_CHOICES,attrs={'class': 'form-control'}),
        }


class MessageForm(forms.ModelForm):

    class Meta:

        model = Message

        fields = (
            'user', 
            'person', 
            'title', 
            'body', 
            'author', 
            )