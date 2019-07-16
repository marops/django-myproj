import django_tables2 as tables
from .models import Article
from django_tables2.utils import A
from django.utils.html import format_html

class ArticleTable(tables.Table):
    action = tables.LinkColumn('myapp:article_details', args=[A('pk')], text='edit')
    edit = tables.Column(empty_values=())

    def render_edit(self,value,record):
        l='<a href="/article_edit/%d">%s</a>' % (record.id,record.headline)
        return format_html(l)

    class Meta:
        model = Article
        #exclude = ['id','content']
        fields = ('headline','pub_date','reporter',)
        template_name = 'django_tables2/bootstrap.html'

