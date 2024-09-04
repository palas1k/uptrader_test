from django.db import models


# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    url = models.CharField(max_length=255, blank=True, null=True, verbose_name='URL')
    named_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='Named URL')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Родитель')
    menu_name = models.CharField(max_length=255, verbose_name='Название меню')

    def __str__(self):
        return self.name


    @property
    def children(self):
        return self.menuitem_set.all()