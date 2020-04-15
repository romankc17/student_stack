from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	city = models.CharField(max_length=50, blank=True)
	college = models.CharField(max_length=100, blank=True)
	contact = models.IntegerField(blank=True)

	SEMESTER_CHOICES = (
		("1", "1"),
		("2", "2"),
		("3", "3"),
		("4", "4"),
		("5", "5"),
		("6", "6"),
		("7", "7"),
		("8", "8"),
	)
	semester = models.CharField(
		max_length=20,
		choices=SEMESTER_CHOICES,
		blank=True
	)

	image = models.ImageField(default ='default.jpg', upload_to='profile_pics', )
	#To use ImageField first we have to install Pillow (PIL)

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)

		img = Image.open(self.image.path)

		if img.height > 200 or img.width > 200:
			output_size = (200, 200)
			img.thumbnail(output_size)
			img.save(self.image.path)   