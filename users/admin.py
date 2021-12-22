#mysite/admin.py
#----

from django.contrib import admin
from django.contrib.auth import get_user_model
from authemail.admin import EmailUserAdmin
from .models import CustomUser as CU
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin

class MyUserAdmin(EmailUserAdmin):
    fieldsets = (
        (None,
            {'fields':
                ('email', 'password')
            }
        ),
        ('Personal Info',
            {'fields':
                ('first_name', 'last_name')
            }
        ),
        ('Permissions',
            {'fields':
                ('is_active', 'is_staff','is_superuser', 'is_verified', 'groups','user_permissions')
            }
        ),
        ('Important dates',
            {'fields':
                ('last_login', 'date_joined')
            }
        ),
        ('Custom info',
            {'fields':
                ('age','can_upload_images','user_flair',)
            }
        ),
    )
    list_filter = ['is_superuser','is_staff','is_active','is_verified']

admin.site.unregister(get_user_model(),)
admin.site.register(get_user_model(), MyUserAdmin)
admin.site.register(Token,TokenAdmin)
