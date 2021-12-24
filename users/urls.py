from django.urls import path, re_path, include
from .api_views import CustomVerify, CustomLogin, CustomLogout, CustomPasswordResetVerify, CustomPasswordResetVerified, CustomPasswordChange

urlpatterns = [
    re_path(r'^signup/verify/$',CustomVerify.as_view(),name="custom-verify"),
    re_path(r'^login/$',CustomLogin.as_view(),name='custom-login'),
    re_path(r'^logout/$',CustomLogout.as_view(),name='custom-logout'),
    re_path(r'^password/reset/verify/$',CustomPasswordResetVerify.as_view(),name='custom-password-reset-verify'),
    re_path(r'^password/reset/verified/$', CustomPasswordResetVerified.as_view(), name='custom-password-reset-verified'),
    re_path(r'^password/change/$',CustomPasswordChange.as_view(), name='custom-password-change'),
    path('',include('authemail.urls')),
]
