from django.shortcuts import render_to_response
from django.template import RequestContext

from base.models import Candidate

def home(request):
    cs = Candidate.objects.all().order_by('id')
    return render_to_response(
        'home.html',
        {'cs': cs, },
        context_instance = RequestContext(request),
    )

def popup(request):
    cs = Candidate.objects.all().order_by('id')
    return render_to_response(
        'popup.html',
        {'cs': cs, },
        context_instance = RequestContext(request),
    )
