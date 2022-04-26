from django.http import HttpResponse

from api.loop import webhook


def handle(request):
    webhook.feed(request.body)
    return HttpResponse("OK")
