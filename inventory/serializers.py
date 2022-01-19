import inventory
from rest_framework import serializers
from taggit.serializers import (TagListSerializerField,TaggitSerializer)

from .models import Inventory

# Serializer specifying how to convert all the complex Python types into json
# Serializer shortcuts exist but because I'm using taggit to handle my tags I need to manually specify the corresponding serializer
# Manually specifying serializer also makes it easier to customize fields without relying on model level validation

class InventorySerializerVersion1(TaggitSerializer,serializers.Serializer):
    # Specifies the correct serializer and does validation
    pk = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    name = serializers.CharField(
        max_length=100, allow_null=False, allow_blank=False)
    amount = serializers.IntegerField(allow_null=False,min_value=0,max_value=100000)
    description = serializers.CharField(allow_blank=True, required=False)
    msrp = serializers.DecimalField(max_digits=12,decimal_places=2,min_value=0,default=0,required=False)
    tags = TagListSerializerField(default=[])

    def create(self,validated_data):
        """
        Takes in only validated data and creates a new Inventory object which is then returned
        """

        # Add tags manually to invoke taggit's tag manager
        # Validated data will always have at least an empty tag so there's no need to error check
        tags = validated_data.pop('tags')
        inventory = Inventory.objects.create(**validated_data)
        inventory.tags.add(*tags)
        return inventory

    
    def update(self,instance,validated_data):
        """
        Takes in only validated data and updates an existing Inventory object
        Instance that is passed in must exist handling error case if somoneone tries to update an item that doesn't exist
        """

        instance.name = validated_data.get('name',instance.name)
        instance.amount = validated_data.get('amount',instance.amount)
        instance.description = validated_data.get('description',instance.description)
        instance.msrp = validated_data.get('msrp',instance.msrp)

        # Remove all tags and only add new ones to maintain idempotency
        if "tags" in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags,clear=True)
        
        instance.save()
        return instance