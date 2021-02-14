from django.db import models

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


class CustomUser(models.Model):
    u_id = models.DecimalField(primary_key=True, max_digits=9, decimal_places=0)
    email = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=50)
    username = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'custom_user'


class Favourite(models.Model):
    u = models.OneToOneField(CustomUser, models.DO_NOTHING, primary_key=True)
    t = models.ForeignKey('Title', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'favourite'
        unique_together = (('u', 't'),)


class History(models.Model):
    u = models.OneToOneField(CustomUser, models.DO_NOTHING, primary_key=True)
    t = models.ForeignKey('Title', models.DO_NOTHING)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'history'
        unique_together = (('u', 't'),)


class Person(models.Model):
    p_id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'person'


class Principals(models.Model):
    t = models.OneToOneField('Title', models.DO_NOTHING, primary_key=True)
    ordering = models.IntegerField()
    p = models.ForeignKey(Person, models.DO_NOTHING)
    category = models.CharField(max_length=15)
    characters = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'principals'
        unique_together = (('t', 'ordering'),)


class Review(models.Model):
    u = models.OneToOneField(CustomUser, models.DO_NOTHING, primary_key=True)
    t = models.ForeignKey('Title', models.DO_NOTHING)
    time = models.DateTimeField()
    rating = models.FloatField(blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review'
        unique_together = (('u', 't', 'time'),)


class SampleNameBasics(models.Model):
    nconst = models.CharField(primary_key=True, max_length=10)
    primaryname = models.CharField(max_length=50)
    birthyear = models.IntegerField()
    deathyear = models.CharField(max_length=10, blank=True, null=True)
    primaryprofession = models.CharField(max_length=100, blank=True, null=True)
    knownfortitles = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sample_name_basics'


class SampleTitleBasics(models.Model):
    tconst = models.CharField(primary_key=True, max_length=10)
    titletype = models.CharField(max_length=20)
    primarytitle = models.CharField(max_length=200)
    originaltitle = models.CharField(max_length=200)
    isadult = models.BooleanField()
    startyear = models.IntegerField()
    endyear = models.CharField(max_length=10, blank=True, null=True)
    runtimeminites = models.CharField(max_length=10, blank=True, null=True)
    genres = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sample_title_basics'


class SampleTitlePrincipals(models.Model):
    tconst = models.CharField(primary_key=True, max_length=10)
    ordering = models.IntegerField()
    nconst = models.CharField(max_length=10)
    category = models.CharField(max_length=30)
    job = models.CharField(max_length=30, blank=True, null=True)
    characters = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sample_title_principals'
        unique_together = (('tconst', 'ordering'),)


class SampleTitleRatings(models.Model):
    tconst = models.CharField(primary_key=True, max_length=255)
    averagerating = models.FloatField(blank=True, null=True)
    numvotes = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sample_title_ratings'


class Title(models.Model):
    t_id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20, blank=True, null=True)
    genre = models.TextField(blank=True, null=True)  # This field type is a guess.
    release_year = models.IntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)
    isadult = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'title'


