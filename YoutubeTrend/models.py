from django.db import models


class File(models.Model):
    filename = models.TextField(db_column='fileName', blank=True, null=True)  # Field name made lowercase.
    filelocation = models.TextField(db_column='fileLocation', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(auto_now_add=True)
    iduser = models.IntegerField(db_column='idUser', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'file'