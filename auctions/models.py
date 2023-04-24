from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    #It inherits from the AbstractUser and aleready has
    #the fields username, pass, email
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    img = models.CharField(max_length=1000, null=True, blank=True)
    text = models.CharField(max_length=120)
    starting_price = models.FloatField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="owner")
    is_active = models.BooleanField(default=True)
    category = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f"Item {self.id}: {self.title}"

class Comment(models.Model):
    content = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="author")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="object")

    def __str__(self):
        return f"Item {self.id}: {self.content}"

class Watchlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="person")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="item")

    def __str__(self):
        return f"Item {self.id} for {self.owner}: {self.item}"

class Bid(models.Model):
    bid_maker = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="betmaker")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True)
    value = models.FloatField(null=True)

    def __str__(self):
        return f"{self.bid_maker} put {self.value} on item: {self.item.title}"
