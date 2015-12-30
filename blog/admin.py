from django.contrib import admin
from .models import Post
from .models import NumberFact

admin.site.register(Post)
admin.site.register(NumberFact)