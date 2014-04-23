# vim: set ts=2 expandtab:
# Create your views here.
from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from weeabot.webserver.models import WeeabotUserForm
from weeabot.webserver.models import UserForm

def home(request):
  t = loader.get_template('webserver/index.html')
  c = RequestContext(request)
  return HttpResponse(t.render(c))

@login_required
def profile(request):
  if request.method == 'POST': # If the form has been submitted...
    # ContactForm was defined in the previous section
    #form = UserForm(data=request.POST, instance=request.user)
    uform = UserForm(data = request.POST, instance=request.user)
    pform = WeeabotUserForm(data = request.POST, instance=request.user.django_)
    if uform.is_valid() and pform.is_valid():
      user = uform.save()
      profile = pform.save(commit = False)
      profile.user = user
      profile.save()
    return HttpResponseRedirect('/') # Redirect after POST
  else:
    form = WeeabotUserForm(instance=request.user.django_)
    userform = UserForm(instance=request.user)
    t = loader.get_template('webserver/profile.html')
    c = RequestContext(request,
      { 
        'form' : form,
        'userform' : userform, 
      }
    )
    return HttpResponse(t.render(c))
