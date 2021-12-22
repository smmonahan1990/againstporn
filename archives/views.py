from .forms import ReportForm
from django.shortcuts import reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

@permission_required('archives.add_report')
def create_report(request, *args, **kwargs):
    form = ReportForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        obj = form.instance.content_object
        messages.add_message(request, messages.SUCCESS, 'Report sent.')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

