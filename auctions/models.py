from django.contrib.auth.models import AbstractUser
from django.db import models

GENDER_CHOICES = (
   ('M', 'Male'),
   ('F', 'Female')
)

class User(AbstractUser):
    pass
    perfil_image = models.ImageField(upload_to="upload/images/perfil_image/")


class Auction(models.Model):

    #...

    auction_title = models.CharField(max_length=30)
    auction_desc = models.CharField(max_length=255)
    initial_bids = models.FloatField()
    auction_url_img = models.ImageField(upload_to="upload/images/auctions/")
    auction_category = models.CharField(max_length=30)
    created_at = models.DateField()
    created_by = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    auction_state = models.BooleanField(default=True)

    def __str__(self):
        return self.auction_title
    


class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    auction =  models.ManyToManyField(Auction)

    def __str__(self):
        return f"{self.user}"







class Bid(models.Model):
    #..
    bids_user =  models.ForeignKey(User,on_delete= models.CASCADE)
    bids_value = models.FloatField()
    bids_auction = models.ForeignKey(Auction,on_delete = models.CASCADE)
    
    


class Comment(models.Model):
    #..
    auction = models.ForeignKey(Auction, on_delete= models.CASCADE)
    comment = models.CharField(max_length=255)
    comment_author = models.ForeignKey(User, on_delete = models.DO_NOTHING)

    def __str__(self):
        return f"{self.comment} - {self.comment_author}"


