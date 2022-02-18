from accounts.api.serializers import UserSerializer, UserSerializerForFriendship
from friendships.models import Friendship
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class FollowerSerializer(serializers.ModelSerializer):
    #check model here first for fields
    user = UserSerializerForFriendship(source='from_user')
    # created_at = serializers.DateTimeField()

    class Meta:
        model = Friendship
        #fields for user
        fields = ('user', 'created_at')


class FollowingSerializer(serializers.ModelSerializer):
    #check model here first for fields
    user = UserSerializerForFriendship(source='to_user')
    # created_at = serializers.DateTimeField()

    class Meta:
        model = Friendship
        #fields for user
        fields = ('user', 'created_at')

class FriendshipSerializerForCreate(serializers.ModelSerializer):
    #check model here first for fields
    from_user_id = serializers.IntegerField()
    to_user_id = serializers.IntegerField()


    class Meta:
        model = Friendship
        fields = ('from_user_id', 'to_user_id')

    def validate(self, attrs):
        if attrs['from_user_id'] == attrs['to_user_id']:
            raise ValidationError(
                {
                    'message': 'You could not follow yourself'
                }
            )

        if Friendship.objects.filter(
            from_user_id=attrs['from_user_id'],
            to_user_id=attrs['to_user_id'],
        ).exists():
            raise ValidationError({
                'message': "You have alreayd followed this user"
            })
        return attrs

    def create(self, validated_data):
        return Friendship.objects.create(
            from_user_id=validated_data['from_user_id'],
            to_user_id=validated_data['to_user_id'],
        )
