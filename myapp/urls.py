from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import ArticleList, ArticleListBS4
from django.views.generic import TemplateView

from . import views

app_name='myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.MyView.as_view(),name='myapp-about'),
]

urlpatterns += [
    path('articles/<int:year>/', views.year_archive),
    #path('articles/<int:year>/<int:month>/', views.month_archive),
    #path('articles/<int:year>/<int:month>/<int:pk>/', views.article_detail),
    path('article/<int:pk>/', views.article_details, name="article_details"),
]

urlpatterns += [
    path('art/', ArticleList.as_view()),
    path('art/<int:pk>', views.get_article,name='art-detail'),
    path('artbs4',ArticleListBS4.as_view()),
    #path('your-name/', views.get_name),
    path('your-name/', views.MyFormView.as_view()),
    path('your-namebs4/', views.MyFormView.as_view(template_name='myapp/namebs4.html')),
    path('list/',views.list),
    path('asj/',views.asj),
    path('datatablesdata/',views.DatatablesViewData.as_view(), name="datatablesdata"),
    path('datatables/', views.DatatablesView.as_view()),
    path('tables2/',views.tables2)
]


from myapp.views import AuthorCreate, AuthorDelete, AuthorUpdate
urlpatterns += [
    # ...
    path('author/add/', AuthorCreate.as_view(), name='author-add'),
    path('author/<int:pk>/', AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', AuthorDelete.as_view(), name='author-delete'),
    path('author/view/<int:pk>/', views.author_details, name='author-detail'),
]

from .views import Person, ArticleEdit
urlpatterns += [
    path('person/',views.PersonListView.as_view(),name='myapp-person'),
    path('person/<int:pk>/', views.Person, name='myapp-person-pk'),
    #path('person/<int:pk>/delete/',views.PersonDelete.as_view()),
    path('person/<int:pk>/<str:action>/',views.Person),

    path('article_edit/<int:pk>',views.ArticleEdit),
    path('article_edit/<int:pk>/<str:action>/',views.ArticleEdit),
]


