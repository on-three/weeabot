# vim: set ts=2 expandtab:
# Create your views here.
from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def home(request):
  t = loader.get_template('webserver/index.html')
  c = RequestContext(request,
  {
    'user' : request.user,
  })
  return HttpResponse(t.render(c))

@login_required
def profile(request):
  t = loader.get_template('webserver/profile.html')
  c = RequestContext(request,
  {
    'user' : request.user,
  })
  return HttpResponse(t.render(c))
