"""Todo serializers with proper field validation and documentation."""

from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    """Serializer for Todo model with explicit field listing and validation.
    
    This serializer ensures:
    - Only intended fields are exposed
    - Input validation is performed
    - Read-only fields are properly marked
    - Error messages are clear and user-friendly
    """
    
    # Read-only fields
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    # Writable fields with validation
    title = serializers.CharField(
        max_length=255,
        required=True,
        trim_whitespace=True,
        help_text="Todo title (required, max 255 characters)"
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Optional detailed description of the todo"
    )
    completed = serializers.BooleanField(
        required=False,
        default=False,
        help_text="Whether the todo is completed"
    )
    priority = serializers.ChoiceField(
        choices=['low', 'medium', 'high'],
        default='low',
        help_text="Priority level of the todo"
    )
    due_date = serializers.DateTimeField(
        required=False,
        allow_null=True,
        help_text="Optional due date for the todo"
    )

    class Meta:
        model = Todo
        fields = [
            'id', 'title', 'description', 'completed',
            'due_date', 'priority', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_title(self, value):
        """Ensure title is not empty after stripping whitespace."""
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty or contain only whitespace.")
        return value

    def validate_priority(self, value):
        """Validate priority field."""
        valid_priorities = ['low', 'medium', 'high']
        if value not in valid_priorities:
            raise serializers.ValidationError(
                f"Priority must be one of: {', '.join(valid_priorities)}"
            )
        return value

    def validate(self, data):
        """Cross-field validation."""
        # Ensure title exists and is not empty
        if 'title' in data:
            title = data['title'].strip() if isinstance(data['title'], str) else data['title']
            if not title:
                raise serializers.ValidationError({'title': 'Title cannot be empty.'})
            data['title'] = title
        
        return data


class TodoListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list endpoints - returns only essential fields."""
    
    class Meta:
        model = Todo
        fields = ['id', 'title', 'completed', 'priority', 'due_date', 'created_at']
        read_only_fields = ['id', 'created_at']


class TodoPartialUpdateSerializer(serializers.ModelSerializer):
    """Serializer for PATCH requests - all fields optional."""
    
    title = serializers.CharField(required=False, max_length=255, trim_whitespace=True)
    description = serializers.CharField(required=False, allow_blank=True)
    completed = serializers.BooleanField(required=False)
    priority = serializers.ChoiceField(required=False, choices=['low', 'medium', 'high'])
    due_date = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Todo
        fields = ['title', 'description', 'completed', 'due_date', 'priority']

    def validate_title(self, value):
        """Ensure title is not empty if provided."""
        if value and not value.strip():
            raise serializers.ValidationError("Title cannot be empty or contain only whitespace.")
        return value
