# This is an auto-generated Django model module.

# You'll have to do the following manually to clean this up:

#   * Rearrange models' order

#   * Make sure each model has one field with primary_key=True

#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior

#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table

# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models


class AuthGroup(models.Model):

    name = models.CharField(unique=True, max_length=150)

    class Meta:

        managed = False

        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):

    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:

        managed = False

        db_table = 'auth_group_permissions'

        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):

    name = models.CharField(max_length=255)

    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)

    codename = models.CharField(max_length=100)

    class Meta:

        managed = False

        db_table = 'auth_permission'

        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):

    password = models.CharField(max_length=128)

    last_login = models.DateTimeField(blank=True, null=True)

    is_superuser = models.IntegerField()

    username = models.CharField(unique=True, max_length=150)

    first_name = models.CharField(max_length=150)

    last_name = models.CharField(max_length=150)

    email = models.CharField(max_length=254)

    is_staff = models.IntegerField()

    is_active = models.IntegerField()

    date_joined = models.DateTimeField()

    class Meta:

        managed = False

        db_table = 'auth_user'


class AuthUserGroups(models.Model):

    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:

        managed = False

        db_table = 'auth_user_groups'

        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):

    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:

        managed = False

        db_table = 'auth_user_user_permissions'

        unique_together = (('user', 'permission'),)


class BidCrawling(models.Model):

    objects = models.Manager()

    bid = models.IntegerField(primary_key=True)

    title = models.TextField(blank=True, null=True)

    writer = models.TextField(blank=True, null=True)

    translator = models.TextField(blank=True, null=True)

    painter = models.TextField(blank=True, null=True)

    publisher = models.TextField(blank=True, null=True)

    # Field name made lowercase.
    publishdate = models.DateField(
        db_column='publishDate', blank=True, null=True)

    intro = models.TextField(blank=True, null=True)

    content = models.TextField(blank=True, null=True)

    # Field name made lowercase.
    authorintro = models.TextField(
        db_column='authorIntro', blank=True, null=True)

    # Field name made lowercase.
    categorytop = models.TextField(
        db_column='categoryTop', blank=True, null=True)

    # Field name made lowercase.
    categorymiddle = models.TextField(
        db_column='categoryMiddle', blank=True, null=True)

    # Field name made lowercase.
    categorybottom = models.TextField(
        db_column='categoryBottom', blank=True, null=True)

    # Field name made lowercase.
    isbn = models.TextField(db_column='ISBN', blank=True, null=True)

    grade = models.IntegerField(blank=True, null=True)

    review = models.TextField(blank=True, null=True)

    image = models.TextField(blank=True, null=True)

    class Meta:

        managed = False

        db_table = 'bid_crawling'

        ordering = ['-bid']


class BookBook(models.Model):

    title = models.CharField(max_length=50)

    publication_date = models.DateField(blank=True, null=True)

    author = models.CharField(max_length=30)

    price = models.DecimalField(max_digits=5, decimal_places=2)

    pages = models.IntegerField(blank=True, null=True)

    book_type = models.PositiveSmallIntegerField()

    timestamp = models.DateField()

    class Meta:

        managed = False

        db_table = 'book_book'


class BookCrawling(models.Model):

    objects = models.Manager()

    # Field name made lowercase.
    searchsubject = models.CharField(
        db_column='searchSubject', max_length=500, blank=True, null=True)

    title = models.CharField(max_length=500, blank=True, null=True)

    writer = models.CharField(max_length=500, blank=True, null=True)

    translator = models.CharField(max_length=500, blank=True, null=True)

    painter = models.CharField(max_length=500, blank=True, null=True)

    publisher = models.CharField(max_length=500, blank=True, null=True)

    # Field name made lowercase.
    publishdate = models.DateField(
        db_column='publishDate', blank=True, null=True)

    intro = models.TextField(blank=True, null=True)

    content = models.TextField(blank=True, null=True)

    # Field name made lowercase.
    authorintro = models.TextField(
        db_column='authorIntro', blank=True, null=True)

    # Field name made lowercase.
    categorytop = models.CharField(
        db_column='categoryTop', max_length=500, blank=True, null=True)

    # Field name made lowercase.
    categorymiddle = models.CharField(
        db_column='categoryMiddle', max_length=500, blank=True, null=True)

    # Field name made lowercase.
    categorybottom = models.CharField(
        db_column='categoryBottom', max_length=500, blank=True, null=True)

    bid = models.IntegerField(blank=True, null=True)

    # Field name made lowercase.
    isbn = models.CharField(
        db_column='ISBN', max_length=50, blank=True, null=True)

    grade = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)

    review = models.IntegerField(blank=True, null=True)

    image = models.CharField(max_length=5000, blank=True, null=True)

    class Meta:

        managed = False

        db_table = 'book_crawling'

        ordering = ['-id']


class Bottomcateogry(models.Model):

    # Field name made lowercase.
    bottomcategoryname = models.TextField(
        db_column='bottomCategoryName', blank=True, null=True)

    # Field name made lowercase.
    bottomcategorynum = models.TextField(
        db_column='bottomCategoryNum', blank=True, null=True)

    # Field name made lowercase.
    middlecategorynum = models.TextField(
        db_column='middleCategoryNum', blank=True, null=True)

    # Field name made lowercase.
    topcategorynum = models.TextField(
        db_column='topCategoryNum', blank=True, null=True)

    class Meta:

        managed = False

        db_table = 'bottomcateogry'


class DjangoAdminLog(models.Model):

    action_time = models.DateTimeField()

    object_id = models.TextField(blank=True, null=True)

    object_repr = models.CharField(max_length=200)

    action_flag = models.PositiveSmallIntegerField()

    change_message = models.TextField()

    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)

    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:

        managed = False

        db_table = 'django_admin_log'


class DjangoContentType(models.Model):

    app_label = models.CharField(max_length=100)

    model = models.CharField(max_length=100)

    class Meta:

        managed = False

        db_table = 'django_content_type'

        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):

    app = models.CharField(max_length=255)

    name = models.CharField(max_length=255)

    applied = models.DateTimeField()

    class Meta:

        managed = False

        db_table = 'django_migrations'


class DjangoSession(models.Model):

    session_key = models.CharField(primary_key=True, max_length=40)

    session_data = models.TextField()

    expire_date = models.DateTimeField()

    class Meta:

        managed = False

        db_table = 'django_session'


class Middlecategory(models.Model):

    # Field name made lowercase.
    middlecategoryname = models.TextField(
        db_column='middleCategoryName', blank=True, null=True)

    # Field name made lowercase.
    middlecategorynum = models.TextField(
        db_column='middleCategoryNum', blank=True, null=True)

    # Field name made lowercase.
    topcategorynum = models.TextField(
        db_column='topCategoryNum', blank=True, null=True)

    class Meta:

        managed = False

        db_table = 'middlecategory'


class Task(models.Model):

    objects = models.Manager()

    # Field name made lowercase.
    taskid = models.IntegerField(db_column='taskId', blank=True, null=True)

    # Field name made lowercase.
    taskcontent = models.CharField(
        db_column='taskContent', max_length=5000, blank=True, null=True)

    str_time = models.DateTimeField(blank=True, null=True)

    end_time = models.DateTimeField(blank=True, null=True)

    complete = models.CharField(max_length=50, blank=True, null=True)

    # Field name made lowercase.
    errordetail = models.CharField(
        db_column='errorDetail', max_length=5000, blank=True, null=True)

    # Field name made lowercase.
    crawlernum = models.IntegerField(
        db_column='crawlerNum', blank=True, null=True)

    class Meta:

        managed = False

        db_table = 'task'


class Topcategory(models.Model):

    # Field name made lowercase.
    tobcategoryname = models.TextField(
        db_column='tobCategoryName', blank=True, null=True)

    # Field name made lowercase.
    topcategorynum = models.TextField(
        db_column='topCategoryNum', blank=True, null=True)

    class Meta:

        managed = False

        db_table = 'topcategory'


class WriterInfo(models.Model):

    num = models.TextField(blank=True, null=True)

    name = models.TextField(blank=True, null=True)

    # Field name made lowercase.
    booktitle = models.TextField(db_column='bookTitle', blank=True, null=True)

    bid = models.TextField(blank=True, null=True)

    isbn = models.TextField(blank=True, null=True)

    link = models.TextField(blank=True, null=True)

    class Meta:

        managed = False

        db_table = 'writer_info'


class Book(models.Model):
    objects = models.Manager()
    HARDCOVER = 1
    PAPERBACK = 2
    EBOOK = 3
    BOOK_TYPES = (
        (HARDCOVER, 'Hardcover'),
        (PAPERBACK, 'Paperback'),
        (EBOOK, 'E-book'),
    )
    title = models.CharField(max_length=50)
    publication_date = models.DateField(null=True)
    author = models.CharField(max_length=30, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pages = models.IntegerField(blank=True, null=True)
    book_type = models.PositiveSmallIntegerField(choices=BOOK_TYPES)

    timestamp = models.DateField(auto_now_add=True, auto_now=False)
