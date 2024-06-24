from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse


class Block(models.Model):
    title = models.CharField(max_length=3, verbose_name='Блок', unique=True)
    slug = models.SlugField(max_length=4, verbose_name='Url')
    user = models.ManyToManyField(User, verbose_name='Пользователь', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('block_chat', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Блок'
        verbose_name_plural = 'Блоки'
        ordering = ['title']


class BlockMessages(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE, verbose_name='Блок', default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return 'Сообщение от ' + str(self.user) + ': ' + str(self.text)

    class Meta:
        verbose_name = 'Сообщение блока'
        verbose_name_plural = 'Сообщения блока'
        ordering = ['-date_added']


class Duty(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE, verbose_name='Блок', default='')
    sending_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    responsible_person = models.CharField(max_length=50, verbose_name="Ответственный человек")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    duty_date = models.DateField(verbose_name='Дата дежурства')
    room = models.CharField(max_length=3, verbose_name='Комната')

    def __str__(self):
        return "Блок " + self.block.title + ", Комната " + self.room + ", Время " + str(self.duty_date)

    class Meta:
        verbose_name = 'Дежурство'
        verbose_name_plural = 'Дежурства'
        ordering = ['-duty_date']


class ImageDuty(models.Model):
    duty = models.ForeignKey(Duty, on_delete=models.CASCADE, null=True, verbose_name='Дежурство')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')


class Ads(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_ad', kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']


class ImageAd(models.Model):
    ad = models.ForeignKey(Ads, on_delete=models.CASCADE, null=True, verbose_name='Объявление')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')


class CommentAds(models.Model):
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE, verbose_name='Объявление')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        ordering = ['-date_added']


class GeneralChatMessages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return 'Сообщение от ' + str(self.user) + ': ' + str(self.text)

    class Meta:
        verbose_name = 'Сообщение общего чата'
        verbose_name_plural = 'Сообщение общего чата'
        ordering = ['-date_added']


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='Контент')
    likes = models.ManyToManyField(User, blank=True, related_name='Лайки', verbose_name='Лайки')
    dislikes = models.ManyToManyField(User, blank=True, related_name='Дизлайки', verbose_name='Дизлайки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_news', kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']


class ImageNews(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, null=True, verbose_name='Новость')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')


class CommentNews(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='Новость')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        ordering = ['-date_added']
