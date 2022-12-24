from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    first_name = models.CharField(verbose_name="Имя", max_length=150)
    last_name = models.CharField(verbose_name="Фамилия", max_length=150)
    email = models.EmailField(verbose_name="Электронная почта", null=False, blank=False)
    phoneNumber = PhoneNumberField(verbose_name="Номер телефона", unique=True, null=False, blank=False)

    def __str__(self):
        return f'{self.first_name, self.last_name}'


class Area(models.Model):
    title = models.CharField(verbose_name="Горный Хребет", max_length=150)

    def __str__(self):
        return f'{self.title}'


class MountainPass(models.Model):
    STATUS = [
        ('new', 'Новый'),
        ('pending', 'В процессе'),
        ('accepted', 'Модерация прошла'),
        ('rejected', 'Модерация не прошла')
    ]
    LEVELS = [
        ('1А', '1А'),
        ('1Б', '1Б'),
        ('2А', '2А'),
        ('2Б', '2Б'),
        ('3А', '3А'),
        ('3Б', '3Б'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(verbose_name="Название", max_length=150)
    title_2 = models.CharField(verbose_name="Альтернативное название", max_length=150, null=True)
    area = models.ForeignKey(Area, verbose_name='Горный хребет', on_delete=models.CASCADE)
    longitude = models.FloatField(verbose_name='Долгота')
    latitude = models.FloatField(verbose_name='Широта')
    height = models.IntegerField(verbose_name="Высота")
    photos = models.FileField(verbose_name="Фото", upload_to='files/', blank=True)
    added_at = models.DateTimeField(verbose_name="Добавлено", auto_now_add=True)
    status = models.CharField(verbose_name="Статус", max_length=200, choices=STATUS, default='new')
    dl_spring = models.CharField(verbose_name="Уровень сложности весной", max_length=2, choices=LEVELS, blank=True)
    dl_summer = models.CharField(verbose_name="Уровень сложности летом", max_length=2, choices=LEVELS, blank=True)
    dl_autumn = models.CharField(verbose_name="Уровень сложности осенью", max_length=2, choices=LEVELS, blank=True)
    dl_winter = models.CharField(verbose_name="Уровень сложности зимой", max_length=2, choices=LEVELS, blank=True)

    def __str__(self):
        return f'{self.title}'
