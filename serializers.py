from rest_framework import serializers
from .models import People

class API(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=People
        fields=['url','EmailId','name']