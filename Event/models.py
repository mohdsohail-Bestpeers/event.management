from django.db import models
from django.contrib.auth.models import User


LOCATION = (
    ("indore", "Indore"),
    ("ujjain", "Ujjain"),
    ("pune", "Pune"),
    ("mumbai", "Mumbai"),
    ("banglore", "Banglore"),
    ("other", "Other"),
)

SERVICE = (
    ("wedding", "Wedding"),
    ("birthday", "BirthDay"),
    ("stage_decoration", "Stage_Decoration"),
)

ROLL = (
    ("publisher","Publisher"),
    ("enduser","EndUser"),
)

'''Handle the Event usertype details in database administrations'''
class UserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='user_type')
    Mobile_no = models.IntegerField()
    roll = models.CharField( choices=ROLL, default="enduser", max_length=100)
 


'''Handle the Event fields details in database administrations'''
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publisher = models.ForeignKey(UserType, on_delete=models.CASCADE)    #show created publisher from the administrations
    service = models.CharField(choices=SERVICE, default="birthday", max_length=50)
    Max_Guest = models.IntegerField(null=True, blank=True)
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
    )
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    description = models.TextField(blank=True)
    payment_status = models.CharField(max_length=20, default='pending')
    user_event_request = models.CharField(max_length=20, default='pending')
    

    def __str__(self):
        return self.service

'''Handle the Address details in database administrations'''
class Address(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_address')
    #city = models.CharField(choices=LOCATION, default="indore", max_length=50)
    city = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pincode = models.IntegerField()

'''image function to store the image in separate id folder'''
def image_path(instance, filename):
    instance_id = instance.event.id
    return "images/{}/{}".format(instance_id, filename)

'''Handle the photos with create or update date in database administrations'''
class event_photo(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="event_photos"
    )
    photo = models.ImageField(upload_to=image_path, max_length=255)
    create_date = models.DateField(auto_now_add=True, null=True)
    update_date = models.DateField(auto_now=True, null=True)
