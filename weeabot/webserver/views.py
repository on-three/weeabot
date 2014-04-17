# vim: set ts=2 expandtab:
# Create your views here.
from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect


def home(request):
  t = loader.get_template('webserver/index.html')
  c = RequestContext(request, {
    })
  return HttpResponse(t.render(c))
