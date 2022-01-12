#mysite/admin.py
#----

from django.contrib import admin
from django.contrib.auth import get_user_model
from authemail.admin import EmailUserAdmin
from .models import CustomUser as CU
from rest_framework.authtoken.models import Token, TokenProxy
from rest_framework.authtoken.admin import TokenAdmin

class MyUserAdmin(EmailUserAdmin):
    fieldsets = (
        (None,
            {'fields':
                ('email', 'password'),
             'classes': ('collapse',),
            }
        ),
        ('Personal Info',
            {'fields':
                ('first_name', 'last_name'),
             'classes': ('collapse',),
            }
        ),
        ('Permissions',
            {'fields':
                ('is_active', 'is_staff','is_superuser', 'is_verified', 'groups','user_permissions'),
             'classes': ('collapse',),
            }
        ),
        ('Important dates',
            {'fields':
                ('last_login', 'date_joined'),
             'classes': ('collapse',),
            }
        ),
        ('Custom info',
            {'fields':
                ('age','can_upload_images','user_flair',),
             'classes': ('collapse',),
            }
        ),
    )
    list_filter = ['is_superuser','is_staff','is_active','is_verified']
    list_display = ['email','is_superuser','is_verified',]
admin.site.unregister(get_user_model(),)
admin.site.unregister(TokenProxy)
admin.site.register(get_user_model(), MyUserAdmin)
admin.site.register(Token,TokenAdmin)
