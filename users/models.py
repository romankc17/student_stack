from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from faculty.models import Category,Batch


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', blank=True, null=True)
	GENDERS=[('M', 'Male'),
			 ('F', 'Female')]
	gender = models.CharField(max_length=1, choices=GENDERS, blank=True, null=True)
	city = models.CharField(max_length=50, blank=True)
	college = models.CharField(max_length=100, blank=True)
	faculty = models.ForeignKey(Category,null=True, blank=True, on_delete=models.SET_NULL)
	batch = models.ForeignKey(Batch, null=True, on_delete=models.SET_NULL)
	image = models.ImageField(default ='boy.png', upload_to='profile_pics')
	#To use ImageField first we have to install Pillow (PIL)

	def __str__(self):
		return f'{self.user.username} Profile'

	# def save(self, *args, **kwargs):
	# 	super(Profile, self).save(*args, **kwargs)
	#
	#
	#
	# 	img = Image.open(self.image.path)
	#
	# 	if img.height > 200 or img.width > 200:
	# 		output_size = (200, 200)
	# 		img.thumbnail(output_size)
	# 		img.save(self.image.path)