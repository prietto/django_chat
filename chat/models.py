# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

# Create your models here.


class Message(models.Model):
    sender_user = models.ForeignKey(User,blank=False, null=False, on_delete=models.CASCADE, related_name='sender_set', verbose_name=_('Emisor'))
    #receiver_user = models.ForeignKey(User,blank=False, null=False, on_delete=models.CASCADE, related_name='receiver_set', verbose_name=_('Receptor'))
    message = models.TextField(blank=True, null=True, verbose_name=_('Mensaje'))
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha de Creación'))
    


    def __str__(self):
        return self.message
    
    class Meta:
        verbose_name="Mensajes"
        ordering=('creation_date',)



