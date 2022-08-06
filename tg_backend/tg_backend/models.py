from django.db import models


class organizers(models.Model):

    id = models.IntegerField(primary_key=True)
    level = models.ForeignKey('level', on_delete=models.PROTECT)
    room = models.ForeignKey('room', on_delete=models.PROTECT)
    surname = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    tg_tag = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=12)
    department = models.TextField()
    texts = models.TextField()


class room(models.Model):

    number = models.CharField(max_length=4, primary_key=True)
    capacity = models.IntegerField()


class guest(models.Model):

    id = models.IntegerField(primary_key=True)
    level = models.ForeignKey('level', on_delete=models.PROTECT)
    surname = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    room = models.ForeignKey('room', on_delete=models.PROTECT)
    tg_tag = models.CharField(max_length=20, unique=True)
    vk_link = models.CharField(max_length=20)
    texts = models.TextField()
    team = models.IntegerField()


class organizer_schedule(models.Model):

    id = models.IntegerField(primary_key=True)
    tg_tag = models.ForeignKey('organizers', on_delete=models.PROTECT, to_field='tg_tag', related_name='tg_tag1')
    desc = models.CharField(max_length=20)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    finish_time = models.TimeField(auto_now=False, auto_now_add=False)
    changer = models.ForeignKey('organizers', on_delete=models.PROTECT, to_field='tg_tag', related_name='tg_tag2')

class guest_schedule(models.Model):

    id = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=20)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)

class level(models.Model):

    id = models.IntegerField(primary_key=True)
    level = models.CharField(max_length=15)


class broadcast(models.Model):

    id = models.IntegerField(primary_key=True)
    level = models.ForeignKey('level', on_delete=models.PROTECT)
    title = models.CharField(max_length=30)
    text = models.TextField()


class issue(models.Model):

    id = models.IntegerField(primary_key=True)
    tg_tag = models.ForeignKey('organizers', on_delete=models.PROTECT, to_field='tg_tag')
    desc = models.TextField()
    status = models.CharField(max_length=256)



class script(models.Model):

    id = models.IntegerField(primary_key=True)
    head = models.TextField()
    text = models.TextField()


class button(models.Model):

    id = models.IntegerField(primary_key=True)
    title_from = models.ForeignKey('script', on_delete=models.CASCADE)
    text = models.TextField()