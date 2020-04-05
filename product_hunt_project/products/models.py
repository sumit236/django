from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=50)
    pub_date = models.DateField()
    url = models.TextField()
    votes_total = models.IntegerField(default=1)
    image = models.ImageField(upload_to='images/')
    icon = models.ImageField(upload_to='images/')
    body = models.TextField()
    # if user gets deleted then all the products associated with that gets deleted as well.
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)


# def __str__(self):
#     return self.title
#
#
# def summary(self):
#     return self.body[:30]
#
#
# def pub_date_pretty(self):
#     return self.pub_date.strftime('%b %e %Y')