from rest_framework import serializers
from .models import User, CompanyProfile, PersonProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            user_type=validated_data['user_type']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PersonSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    # token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = PersonProfile
        fields = ('user', 'name', 'last_name', 'sex', 'age', 'resume', 'fields')
        # read_only_fields = ('token',)

    def create(self, validated_data):
        print(validated_data)
        username = validated_data['user.username']
        email = validated_data['user.email']
        password = validated_data['user.password']
        user_type = 2
        user_data = {'username': username, 'email': email, 'user_type': user_type, 'password': password}
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        # token = Token.objects.create(user=user)
        # self.token = str(token.key)
        person, created = PersonProfile.objects.update_or_create(user=user, name=validated_data.get('name'),
                                                                 last_name=validated_data.get('last_name'),
                                                                 sex=validated_data.get('sex'),
                                                                 age=validated_data.get('age'),
                                                                 resume=validated_data.get('resume'))
        return person


class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    # token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = CompanyProfile
        fields = ('user', 'name', 'creation_year', 'address', 'number', 'fields')
        # read_only_fields = ('token',)

    def create(self, validated_data):
        print(validated_data)
        username = validated_data['user.username']
        email = validated_data['user.email']
        password = validated_data['user.password']
        user_type = 1
        user_data = {'username': username, 'email': email, 'user_type': user_type, 'password': password}
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        # token = Token.objects.create(user=user)
        # self.token = str(token.key)
        company, created = CompanyProfile.objects.update_or_create(user=user, name=validated_data.get('name'),
                                                                   creation_year=validated_data.get('creation_year'),
                                                                   address=validated_data.get('address'),
                                                                   number=validated_data.get('number'))
        return company



