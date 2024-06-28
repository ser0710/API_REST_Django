from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlataform, Review

# def name_length(value):
#         if len(value) < 2:
#             raise serializers.ValidationError("Name is too short!")

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length]) # validators
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
    # def validate_name(self, value): # field level validation
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short!")
    #     else:
    #         return value
    
    # def validate(self, data): # object level validation
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Title and description should be different!")
    #     else:
    #         return data
    
    
        
# Model serializer

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ['watchlist']
        # fields = '__all__'
        

class WatchListSerializer(serializers.ModelSerializer):
    # len_name = serializers.SerializerMethodField()
    # reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source='plataform.name')
    
    class Meta:
        model = WatchList
        fields = "__all__" # to show all properties
        # fields = ['id', 'name', 'description'] define what properties shows
        # exclude = ['active'] exclude a propertie
        
    # def get_len_name(self, object):
    #     length = len(object.name)
    #     return length
        
    # def validate_name(self, value): # field level validation
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short!")
    #     else:
    #         return value
    
    # def validate(self, data): # object level validation
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Title and description should be different!")
    #     else:
    #         return data
    
class StreamPlataformSerializer(serializers.ModelSerializer): # instead of ModelSerializer we can use HyperlinkedModelSerializer
    watchlist = WatchListSerializer(many=True, read_only=True) # same as related_name in the relation in models.py, this shows all the information
    # watchlist = serializers.StringRelatedField(many=True) # shows only strings define in the __str__
    # watchlist = serializers.HyperlinkedRelatedField( # have a link to access to the details of the element
    #     many=True,
    #     read_only=True,
    #     view_name='movie-detail'
    # )
    class Meta:
        model = StreamPlataform
        fields = '__all__'
