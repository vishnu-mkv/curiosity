from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import ProfileImage, PostThumbnail, PostImage


class ProfilePicSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = ProfileImage
        fields = ['image']

#     def create(self, validated_data):
#         image=validated_data.pop('image')
#         return ProfileImage.objects.create(image=image)


class PostThumbnailSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = PostThumbnail
        fields = ['image']


class PostImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    post = serializers.CharField(source='post.slug', read_only=True)

    class Meta:
        model = PostImage
        fields = ['image', 'post']