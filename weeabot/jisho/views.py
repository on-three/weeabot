# vim: set ts=2 expandtab:
# Create your views here.
from django.template import Context, loader
from weeabot.jisho.models import Definition
from django.http import HttpResponse

def home(request):
  definitions = Definition.objects.all()
  t = loader.get_template('jisho/index.html')
  c = Context({
    'definitions': definitions
    })
  return HttpResponse(t.render(c))
