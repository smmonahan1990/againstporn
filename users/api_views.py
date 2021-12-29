from django.contrib import auth
from django.db.models import Q, ObjectDoesNotExist as ODE
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from .models import CustomUser as CU
from datetime import datetime as dt, timezone as tz
import logging, os
import pprint as pp
# api views

from authemail import views
from authemail.models import PasswordResetCode
from rest_framework import status
from rest_framework.authentication import TokenAuthentication as TA
from rest_framework.authtoken.models import Token
from rest_framework.request import ForcedAuthentication as FA
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import csrf_exempt

logger = logging.getLogger(__name__)

debug = lambda x: logger.debug(pp.pformat(x))

class CustomLogin(views.Login):

    def post(self, request, format=None, **kwargs):
        response = super().post(request, format, **kwargs)
        try:
            user = auth.authenticate(request=request, **request.data)
        except TypeError:
            try:
                cred = {'email':request.data['email'][0], 'password':request.data['password'][0]}
                user = auth.authenticate(request=request, **cred)
            except (KeyError, TypeError):
                user = None
        if user:
            auth.login(request, user)
        return response

from rest_framework import exceptions
class CustomLogout(views.Logout):

    def get(self, request, format=None, **kwargs):
        response = super().get(request, format, **kwargs)
        auth.logout(request)
        return response

class CustomVerify(views.SignupVerify):
    def get(self, request, format=None):
        super().get(request,format)
        return HttpResponseRedirect(reverse('index'))
    def post(self, request, format=None):
        try:
            verified = CU.objects.get(Q(email=request.data['email'])&Q(is_verified=True))
            if verified:
                return Response({'success':'user is verified'})
            else:
                pass
        except Exception as e:
            logger.error(e)
        return Response({'failure': 'unable to verify user.'}, status=status.HTTP_404_NOT_FOUND)

class CustomPasswordResetVerify(views.PasswordResetVerify):

    def get(self, request, format=None):
        super().get(request, format)
        request.session.setdefault('code',request.GET.get('code','1'))
        return HttpResponseRedirect(reverse('index'))

    def post(self, request, *args, **kwargs):
        code, user = '', ''
        context = {}
        try:
            code = request.session['code']
            user = CU.objects.get(email=request.data['email'])
            verified = PasswordResetCode.objects.filter(
                Q(user=user)&Q(code=code)
            )
            if verified:
                return Response({'success':'%s' % code})
            else:
                context['failure'] = 'unable to verify password reset code.'
        except Exception as e:
            logger.error(e)
            context['failure'] = str(e)
        return Response(context, status=status.HTTP_404_NOT_FOUND)

class CustomPasswordResetVerified(views.PasswordResetVerified):

    def post(self, request, format=None):
        try:
            code = request.session.get('code')
            request.data.update({'code':code})
            return super().post(request, format)
        except Exception as e:
            return Response({'detail':e}, status=status.HTTP_400_BAD_REQUEST)

class CustomPasswordChange(views.PasswordChange):

    def post(self, request, format=None):
        if request.data.get('verify'):
            try:
                user, _ = TA().authenticate(request)
                user.check_password(request.data['verify'])
                if user:
                    return Response({'success':'user verified.'}, status=status.HTTP_200_OK)
            except TypeError:
                pass
            return Response({'detail':'Unable to verify user with the given credentials.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return super().post(request, format)

#@csrf_exempt
@api_view(['POST'])
def permissions_check(request, *args, **kwargs):
    debug(locals())
    try:
        user, _ = TA().authenticate(request)
        if user:
            response = Response({'success':'User authentication succeeded.'},status=status.HTTP_200_OK)
            for permission in user.get_all_permissions():
                response.set_signed_cookie(*permission.split('.'))
#            response = Response({'success':user.get_all_permissions()}, status=status.HTTP_200_OK)
#            response.set_signed_cookie('test','fuck')
            return response
    except Exception as e:
        logger.error(e)
    return Response({'detail':'Unable to verify user with the given credentials.'}, status=status.HTTP_404_NOT_FOUND)
