from django.db import models
from django.urls import reverse


class Profile(models.Model):

    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=125, verbose_name='Наименование')
    serial = models.CharField(max_length=16, verbose_name='Серийный номер кассы', unique=True, null=True, blank=True)
    enabled = models.BooleanField(verbose_name='Запуск эмулятора разрешён', default=False)
    port = models.IntegerField(unique=True, verbose_name='Порт на котором работает api эмулятора')
    path = models.CharField(max_length=1024, verbose_name='Полный путь к профилю')
    note = models.CharField(max_length=1024, verbose_name='Примечание', null=True, blank=True)

    def __str__(self):
        return 'Profile services on port: ' + str(self.port)

    def get_absolute_url(self):
        return reverse('manager:edit', args=[self.serial])


class Process(models.Model):
    date = models.DateField(auto_now_add=True)
    id_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    pid = models.IntegerField()

    def __str__(self):
        return str(self.pid)
