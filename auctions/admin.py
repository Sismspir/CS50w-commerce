from django.contrib import admin
from .models import Listing
from .models import Comment
from .models import Watchlist
from .models import Bid
# Register your models here.
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Bid)