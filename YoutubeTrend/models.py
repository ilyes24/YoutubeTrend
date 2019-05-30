from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class File(models.Model):
    filename = models.TextField(db_column='fileName', blank=True, null=True)  # Field name made lowercase.
    filelocation = models.TextField(db_column='fileLocation', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(auto_now_add=True)
    iduser = models.IntegerField(db_column='idUser', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'file'


class Operation(models.Model):
    keyword = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    rank_by = models.CharField(max_length=255)
    capture_in = models.IntegerField(null=True)
    quality = models.CharField(null=True,max_length=40)
    created_at = models.DateTimeField(editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operationUser')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(Operation, self).save(*args, **kwargs)


class Video(models.Model):
    video_id = models.CharField(max_length=255)
    video_url = models.CharField(max_length=1000)
    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    description = models.TextField(null=True)
    views = models.IntegerField()
    likes = models.IntegerField()
    comments = models.IntegerField()
    related_to = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='videoOperation')


class Image(models.Model):
    image_name = models.CharField(max_length=255)
    image_location = models.CharField(max_length=1000)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='imageVideo')


class XmlFile(models.Model):
    file_name = models.CharField(max_length=255)
    file_location = models.CharField(max_length=1000)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='fileVideo')
