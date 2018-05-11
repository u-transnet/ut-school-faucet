from django.shortcuts import render
from django.template.response import TemplateResponse


def app_view(request, *args, **kwargs):
    return TemplateResponse(
        request=request,
        template='web/app.html',
        context={}
    )
