from django.contrib.auth.models import User
from django.db import models

class Reporter(models.Model):
    full_name = models.CharField(max_length=70)

    def __str__(self):
        return self.full_name

class Article(models.Model):
    pub_date = models.DateField()
    headline = models.CharField(max_length=200)
    content = models.TextField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline


from django.urls import reverse

class Author(models.Model):
    name = models.CharField(max_length=200, default='todd')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    email = models.EmailField(null=True)

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Person(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    shirt_size=models.CharField(max_length=1,choices=SHIRT_SIZES)

    def __str__(self):
        return self.last_name+", "+self.first_name

