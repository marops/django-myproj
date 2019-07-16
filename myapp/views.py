from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Article
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request, pk=0):
    msg="My App"
    #return HttpResponse("Hello, world. You're at the myapp index.")
    context={'msg': msg}
    return render(request, 'myapp/index.html', context)

from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "myapp/about.html"
    extra_context = {'msg': 'Message goes here...'}

    def get(self, request):
        msg=request.GET.get('msg')
        return render(request, self.template_name,{'msg':msg})



class MyView(View):
    def get(self, request):
        # <view logic>
        return render(request, "myapp/about.html",{'msg':'OK'})

def year_archive(request, year):
    a_list = Article.objects.filter(pub_date__year=year)
    context = {'year': year, 'article_list': a_list}
    return render(request, 'myapp/year_archive.html', context)

@login_required
def article_details(request, pk):
    a = Article.objects.get(id=pk)
    context = {'id': 1, 'article': a}
    #return HttpResponse(context['article'])
    return render(request, 'myapp/article_detail.html', context)

class ArticleList(ListView):
    template_name = 'myapp/article_listBS4.html'
    model = Article
    queryset= Article.objects.all()
    context_object_name = 'articles'
    paginate_by=10

from django.contrib import messages
class ArticleListBS4(ListView):
    template_name = 'myapp/article_list_bs4.html'
    model = Article
    queryset= Article.objects.all()
    context_object_name = 'articles'
    paginate_by=10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #messages.success(self.request, 'Your password was updated successfully!')
        return context

### Forms
from django.http import HttpResponseRedirect
from .forms import NameForm,PersonForm

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/?m=ok')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'myapp/name.html', {'form': form})

class MyFormView(View):
    form_class = NameForm
    initial = {'key': 'value'}
    template_name = 'myapp/name.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/about/?msg=Success')

        return render(request, self.template_name, {'form': form})

from . import models

### Person
def Person(request,pk,action=None):

    success_url="/person"

    if(pk>0):
        instance = models.Person.objects.get(pk=pk)
    else:
        instance = None

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        if(action=='delete'):
            instance.delete()
            return HttpResponseRedirect(success_url)

        # create a form instance and populate it with data from the request:
        form = PersonForm(request.POST,instance=instance)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()

            # redirect to a new URL:
            return HttpResponseRedirect(success_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        if(action=="delete"):
            #instance = models.Person.objects.get(pk=pk)
            return render(request, 'myapp/confirm_delete.html', {'object': instance,'success_url':success_url})

        form = PersonForm(instance=instance)

    return render(request, 'myapp/person.html', {'form': form, 'rid':pk})

class PersonListView(ListView):

    template_name = 'myapp/person_list.html'
    model = models.Person
    queryset= models.Person.objects.all()
    context_object_name = 'people'
    paginate_by=10

class PersonDelete(DeleteView):
    model = models.Person
    success_url = '/person'
    template_name="myapp/confirm_delete.html"



def get_article(request, pk):
    return HttpResponse("OK")


from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from myapp.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = ['name','created_by']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name','created_by','email']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')

def author_details(request, pk):
    a = Author.objects.get(id=pk)
    context = {'id': 1, 'author': a}
    #return HttpResponse(context['article'])
    return render(request, 'myapp/author_detail.html', context)

def list(request):
    a = Article.objects.all()
    context = {'articles': a}
    return render(request, 'myapp/list.html', context)


from django.core import serializers

def asj(request):
    object_list = Article.objects.all() #or any kind of queryset
    json = serializers.serialize('json', object_list)
    return HttpResponse(json, content_type='application/json')


### Datatables
from django_datatables_view.base_datatable_view import BaseDatatableView

class DatatablesViewData(BaseDatatableView):
    model = Article
    columns = ['id','headline','pub_date','reporter']
    order_columns = ['id','headline','pub_date','reporter']
    max_display_length = 500
    template_name = "myapp/datatableview.html"

    def filter_queryset(self, qs):
        # simple example:
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(headline__istartswith=search)

        return qs

class DatatablesView(TemplateView):
    template_name = 'myapp/datatables.html'
    headers=['ID','Headline','Pub Date','Reporter']
    extra_context={'headers': headers,'ajax_url':'/datatablesdata'}


### django-tables2

from django_tables2 import RequestConfig
from .tables import ArticleTable

def tables2(request):
    table = ArticleTable(Article.objects.all())
    RequestConfig(request,paginate={'per_page': 10}).configure(table)
    return render(request, 'myapp/tables2.html', {'table': table})


### Article edit
from .forms import ArticleForm

def ArticleEdit(request,pk,action=None):

    success_url="/datatables"

    if(pk>0):
        instance = models.Article.objects.get(pk=pk)
    else:
        instance = None

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        if(action=='delete'):
            instance.delete()
            return HttpResponseRedirect(success_url)

        # create a form instance and populate it with data from the request:
        form = ArticleForm(request.POST,instance=instance)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()

            # redirect to a new URL:
            return HttpResponseRedirect(success_url)

    # if a GET (or any other method) we'll create a blank form
    else:
        if(action=="delete"):
            #instance = models.Person.objects.get(pk=pk)
            return render(request, 'myapp/confirm_delete.html', {'object': instance,'success_url':success_url})

        form = ArticleForm(instance=instance)

    return render(request, 'myapp/article_edit.html', {'form': form, 'rid':pk})


def picture(request):
    return render(request, 'myapp/picture.html', {})

