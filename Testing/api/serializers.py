from rest_framework import serializers
from .models import User, Test, Question, Answer, Category
from django.contrib.auth.hashers import make_password

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['created_by']

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'test_title', 'category', 'status', 'created_at',
                  'updated_at','questions', 'created_by', 'created_by_name',
                  'random_generator', 'number_of_questions', 'keywords']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_created_by_name(self, obj):
        return obj.created_by.name if obj.created_by else None

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ['created_by']

class UserSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type' : 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type' : 'password'}
    )
    
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone_number', 'role', 'type', 
                  'age', 'city', 'avatar', 'interests', 'quiz_points', 
                  'tests_done', 'favorites', 'current_password', 'new_password']
        extra_kwargs = {}


    def create(self, validated_data):
        user = User.objects.create_user(
            name=validated_data['name'],
            password=validated_data['password'],
            email=validated_data['email'],
            role=validated_data.get('role', 'user'),
            type=validated_data['type']
        )
        return user

    def update(self, instance, validated_data):
        current_password = validated_data.pop('current_password', None)
        new_password = validated_data.pop('new_password', None)
        
        if new_password:
            if not instance.check_password(current_password):
                raise serializers.ValidationError(
                    {"current_password" "Current password is incorrect"}
                )
            instance.set_password(new_password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance   
    
class CategoryPercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    