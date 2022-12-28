## В данном проекте я занимался разработкой REST API, которое будет обслуживать мобильное приложение Федерации Спортивного Туризма России (ФСТР).

>###### ФСТР — организация, занимающаяся развитием и популяризацией спортивного туризма в России и руководящая проведением всероссийских соревнований в этом виде спорта.

## Для пользователя в мобильном приложении будут доступны следующие действия:
* Внесение информации о новом объекте (перевале) в карточку объекта.
* Редактирование в приложении неотправленных на сервер ФСТР данных об объектах. На перевале не всегда работает Интернет.
* Заполнение ФИО и контактных данных (телефон и электронная почта) с последующим их автозаполнением при внесении данных о новых объектах.
* Отправка данных на сервер ФСТР.
* Получение уведомления о статусе отправки (успешно/неуспешно).
* Согласие пользователя с политикой обработки персональных данных в случае нажатия на кнопку «Отправить» при отправке данных на сервер.

## Пользователь с помощью мобильного приложения будет передавать в ФСТР следующие данные о перевале:
* координаты перевала и его высота;
* имя пользователя;
* почта и телефон пользователя;
* название перевала;
* несколько фотографий перевала.

>###### Чтобы лучше понимать, как будет работать мобильное приложение, ознакомьтесь с его CJM (customer journey map) по [ссылке](https://docs.google.com/spreadsheets/d/1eNFtPqYUFftQ4v-OC2K91rDGwBfUhsLh3UvEY1CXov0/edit#gid=0).

## Структура моделей для приложения выглядит так:
```
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
```

## REST API для этого приложения рарзаботан при помощи Django Rest Framework, включает в себя методы GET, POST и PATCH и выглядит таким образом:
```
@csrf_exempt
def submitData(request):
    if request.method == 'POST':
        json_params = json.loads(request.body)

        mountain_pass = MountainPass.objects.create(
            title=json_params['title'],
            alt_title=json_params['alt_title'],
            longitude=json_params['longitude'],
            latitude=json_params['latitude'],
            height=json_params['height'],
            images=json_params['images'],
            user=User.objects.create(
                first_name=json_params['first_name'],
                last_name=json_params['last_name'],
                email=json_params['email'],
                phoneNumber=json_params['phoneNumber']

            )

        )
        return HttpResponse(json.dumps({
            "title": mountain_pass.title,
            "alt_title": mountain_pass.alt_title,
            "longitude": mountain_pass.longitude,
            "latitude": mountain_pass.latitude,
            "height": mountain_pass.height,
            "images": mountain_pass.images,
            "user": mountain_pass.user,
        }))


def submitData_get_patch(request, mountain_pass_id):
    mountain_pass = MountainPass.objects.get(id=mountain_pass_id)
    if request.method == 'GET':
        return HttpResponse(json.dumps(
            {
                "title": mountain_pass.title,
                "alt_title": mountain_pass.alt_title,
                "longitude": mountain_pass.longitude,
                "latitude": mountain_pass.latitude,
                "height": mountain_pass.height,
                "images": mountain_pass.images,
                "user": mountain_pass.user,
            }))
    json_params = json.loads(request.body)
    if request.method == 'PATCH':
        mountain_pass.title = json_params.get('title', mountain_pass.title)
        mountain_pass.alt_title = json_params.get('alt_title', mountain_pass.alt_title)
        mountain_pass.longitude = json_params.get('longitude', mountain_pass.longitude)
        mountain_pass.latitude = json_params.get('latitude', mountain_pass.latitude)
        mountain_pass.height = json_params.get('height', mountain_pass.height)
        mountain_pass.images = json_params.get('images', mountain_pass.images)
        mountain_pass.save()
        return HttpResponse(json.dumps({
            "title": mountain_pass.title,
            "alt_title": mountain_pass.alt_title,
            "longitude": mountain_pass.longitude,
            "latitude": mountain_pass.latitude,
            "height": mountain_pass.height,
            "images": mountain_pass.images,
        }))
```
## Проект запущен на виртуальной машине, а также в проекте реализован просмотр структуры REST API при помощи Swagger, который доступен по [этой ссылке](http://84.201.133.27:8000/swagger-docs/)

## Для того, чтобы запустить проект, необходимо установить requirements.txt
`pip install -r requirements.txt`
