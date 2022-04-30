from django.contrib import admin
from .models import SearchResult
from .models import Cluster
from .models import Website
from .models import Quote

admin.site.register(SearchResult)
admin.site.register(Cluster)
admin.site.register(Website)
admin.site.register(Quote)