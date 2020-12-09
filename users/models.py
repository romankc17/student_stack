import os

from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ExifTags
from django.db.models.signals import post_save
from django.dispatch import receiver
from faculty.models import Category,Batch


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', blank=True, null=True)
	GENDERS=[('M', 'Male'),
			 ('F', 'Female')]
	gender = models.CharField(max_length=1, choices=GENDERS, blank=True, null=True)
	city = models.CharField(max_length=50, blank=True)
	college = models.CharField(max_length=100, blank=True)
	faculty = models.ForeignKey(Category,null=True, on_delete=models.SET_NULL)
	batch = models.ForeignKey(Batch, null=True,blank=True, on_delete=models.SET_NULL)
	image = models.ImageField(default ='boy.png', upload_to='profile_pics', null=True, blank=True)
	#To use ImageField first we have to install Pillow (PIL)

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):

		super(Profile, self).save(*args, **kwargs)
		img = Image.open(self.image.path)

		if img.height > 1000 or img.width > 685:
			output_size = (1500,1024)
			img.thumbnail(output_size)
			img.save(self.image.path)

def rotate_image(filepath):
    try:
        image = Image.open(filepath)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
        image.save(filepath)
        image.close()
    except :
        # cases: image don't have getexif
        pass

@receiver(post_save, sender=Profile, dispatch_uid="update_image_profile")
def update_image(sender, instance, **kwargs):
  if instance.image:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fullpath = BASE_DIR + instance.image.url
    rotate_image(fullpath)