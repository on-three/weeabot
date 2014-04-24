# vim: set ts=2 expandtab:
# Create your views here.
from django.template import Context, RequestContext, loader
from weeabot.jisho.models import Definition
from weeabot.jisho.models import VocabularyList
from weeabot.jisho.models import VocabularyListSelectionForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms

def home(request):
  #handling post dropdown result
  if request.method == 'POST':
    list_name = request.POST.get('vlist', '')
    if list_name == '...':
      return HttpResponseRedirect('')
    definition_pk = request.POST.get('definition', '')
    definition = Definition.objects.get(pk=definition_pk)
    new_list = VocabularyList.objects.get(name=list_name)
    definition.lists.add(new_list)
    return HttpResponseRedirect('')

  definitions = Definition.objects.all().order_by('timestamp').reverse()
  first_date = definitions[len(definitions)-1].timestamp
  last_date = definitions[0].timestamp
  lists = VocabularyList.objects.all()
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
  c = RequestContext(request, {
    'title' : 'Weeabot Jisho Lookups',
    'description' : 'Recent weeabot irc bot .jisho lookups',
    'first_date' : first_date,
    'last_date' : last_date,
    'definitions': definitions,
    'paginator' : paginator,
    'lists' : lists,
    })
  return HttpResponse(t.render(c))

def VocabularyListView(request, listname):
  list_object = VocabularyList.objects.get(name=listname)
  
  #handle delte of single list entry
  if request.method == 'POST':
    definition_pk = request.POST.get('definition', '')
    definition = Definition.objects.get(pk=definition_pk)
    definition.lists.remove(list_object)
    return HttpResponseRedirect('')
 
  t = loader.get_template('jisho/vocabulary_list.html')
  c = RequestContext(request, {
    'title' : 'Weeabot Vocabulary List: {name}'.format(name=listname),
    'description' : list_object.desc,
    'list_object' : list_object,
    })
  return HttpResponse(t.render(c))

def VocabularyListsView(request):
  lists = VocabularyList.objects.all()
  t = loader.get_template('jisho/vocab.html')
  c = Context({
    'user' : request.user,
    'title' : 'Current Weeabot Vocabulary Lists',
    'description' : 'Choose a list to view contents.',
    'lists' : lists,
    })
  return HttpResponse(t.render(c))

def NickView(request, nick):
  #handling 'add to vocab list' dropdown
  if request.method == 'POST':
    list_name = request.POST.get('vlist', '')
    if list_name == '...':
      return HttpResponseRedirect('')
    definition_pk = request.POST.get('definition', '')
    definition = Definition.objects.get(pk=definition_pk)
    new_list = VocabularyList.objects.get(name=list_name)
    definition.lists.add(new_list)
    return HttpResponseRedirect('')

  definitions = Definition.objects.all().order_by('timestamp').reverse()
  #only keep those definitions which contain nick of interest
  definitions = [d for d in definitions if d.simple_nick() == nick]
  lists = VocabularyList.objects.all()
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

  t = loader.get_template('jisho/nick.html')
  c = RequestContext(request, {
    'title' : 'Weeabot Lookups by Nick {nick}'.format(nick=nick),
    'description' : 'Current weeabot IRC bot lookups by user with nick {nick}.'.format(nick=nick),
    'nick' : nick,
    'definitions': definitions,
    'paginator' : paginator,
    'lists' : lists,
    })
  return HttpResponse(t.render(c))
