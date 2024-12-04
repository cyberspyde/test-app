from rest_framework import serializers
from .models import User, Test, Question, Answer, Category
        
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
        fields = ['id', 'test_title', 'category', 'status', 'created_at', 'updated_at','questions', 'created_by', 'created_by_name', 'random_generator']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_created_by_name(self, obj):
        return obj.created_by.name if obj.created_by else None

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ['created_by']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password' : {'write_only': True}}

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
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        return super().update(instance,validated_data)
    
class CategoryPercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    