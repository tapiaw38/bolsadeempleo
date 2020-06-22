from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Models
from django.contrib.auth.models import User
from user.models import Person
# Register your models here.
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('pk','user','direction', 'phone_number', 'picture')
    list_display_links = ('pk', 'user')
    list_editable = ('phone_number','direction', 'picture')
    search_fields = ('user__email', 'user__first__name', 'user__last__name','phone_number')
    list_filter = ('user__is_active', 'user__is_staff', 'created', 'modified')
    fieldsets = (
        ('Person', {
            'fields': (('user','picture'),),}),
            ('Extra info',{'fields': (('phone_number',)),}),
            ('Metadata',{'fields':(('created','modified')),}),
        )
    readonly_fields = ('created','modified')

class PersonInLine(admin.StackedInline):
    model = Person
    can_delete = False
    verbose_name_plural = 'persons'

class UserAdmin(BaseUserAdmin):
    inlines = (PersonInLine,)
    list_display = ('username','email','first_name','last_name','is_active','is_staff')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
