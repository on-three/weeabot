# vim: set ts=2 expandtab:
# Create your views here.
from django.template import Context, loader
from weeabot.jisho.models import Definition
from weeabot.jisho.models import VocabularyList
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
  definitions = Definition.objects.all().order_by('timestamp').reverse()
  paginator = Paginator(definitions, 30) # Show 30 contacts per page

  page = request.GET.get('page')
  try:
    definitions = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    definitions = paginator.page(1)
  except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    definitions = paginator.page(paginator.num_pages)

  t = loader.get_template('jisho/index.html')
  c = Context({
    'definitions': definitions,
    'paginator' : paginator
    })
  return HttpResponse(t.render(c))

def VocabularyListView(request, listname):
  list_object = VocabularyList.objects.get(name=listname)
 
  t = loader.get_template('jisho/vocabulary_list.html')
  c = Context({
    'list_object' : list_object,
    })
  return HttpResponse(t.render(c))

def VocabularyListsView(request):
  lists = VocabularyList.objects.all()
  t = loader.get_template('jisho/vocab.html')
  c = Context({
    'lists' : lists,
    })
  return HttpResponse(t.render(c))
