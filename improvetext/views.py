# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed
from django.template import RequestContext
from django.conf import settings

from bundestagger.account.auth import logged_in, is_post

from models import Improvement


@is_post
def apply_improvement(request):
    if not request.user.is_authenticated() or not request.user.is_superuser:
        return HttpResponseForbidden()
    try:
        improvement = Improvement.objects.get(id=int(request.POST["improvement_id"]))
    except (SpeechPart.DoesNotExist, TypeError, KeyError):
        raise Http404
    if request.POST["what"] == "apply":
        improvement.apply()
    else:
        improvement.revert()
    return redirect(request.POST.get("next","/"))
    
