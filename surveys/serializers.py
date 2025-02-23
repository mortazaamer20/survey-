from rest_framework import serializers
from .models import Survey, Question, Response, Answer

class AnswerSerializer(serializers.ModelSerializer):
    # Include question text for clarity in responses
    question_text = serializers.CharField(source='question.text', read_only=True)
    
    class Meta:
        model = Answer
        fields = ['id', 'question', 'question_text', 'text']

class ResponseSerializer(serializers.ModelSerializer):
    # Nest answers to show all details of a response
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Response
        fields = ['id', 'survey', 'first_answer', 'created_at', 'answers']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text']

class SurveySerializer(serializers.ModelSerializer):
    # Nested questions for a complete survey view
    questions = QuestionSerializer(many=True, read_only=True)
    # Optionally, include responses if needed
    responses = ResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Survey
        fields = ['id', 'title', 'questions', 'responses']

# If you need a serializer to output in a comment-style format:
class ResponseDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Response
        fields = ['id', 'first_answer', 'created_at', 'comments']

    def get_comments(self, obj):
        # This returns a list of dicts with each question and its answer.
        return [{
            'question': answer.question.text,
            'answer': answer.text
        } for answer in obj.answers.all()]
