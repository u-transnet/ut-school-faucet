import os

from django.http import HttpResponse
from django.template.response import TemplateResponse

from utschoolfaucet import settings


def service_worker_file_view(request):
    service_worker_file = open(os.path.join(settings.STATIC_ROOT, 'service-worker.js'), 'rb')
    response = HttpResponse(content=service_worker_file)
    response['Content-Type'] = 'application/javascript'
    return response


def app_view(request, *args, **kwargs):
    resp = TemplateResponse(
        request=request,
        template='web/app.html',
        context={}
    )
    resp['Cache-Control'] = 'max-age=86400'

    return resp
