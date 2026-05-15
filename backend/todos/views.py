"""Todo API views with authentication, authorization, and proper error handling."""

import logging
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Todo
from .serializers import TodoSerializer, TodoListSerializer, TodoPartialUpdateSerializer

logger = logging.getLogger(__name__)


class TodoViewSet(viewsets.ModelViewSet):
    """ViewSet for Todo CRUD operations with filtering and pagination.
    
    Endpoints:
    - GET /api/todos/                   - List all todos (paginated, filtered)
    - POST /api/todos/                  - Create new todo
    - GET /api/todos/{id}/              - Retrieve specific todo
    - PUT /api/todos/{id}/              - Full update of todo
    - PATCH /api/todos/{id}/            - Partial update of todo
    - DELETE /api/todos/{id}/           - Delete todo
    - PATCH /api/todos/{id}/complete/   - Mark todo as completed
    
    Query Parameters:
    - ?completed=true/false             - Filter by completion status
    - ?priority=low/medium/high         - Filter by priority
    - ?search=text                      - Search in title and description
    - ?page=1                           - Pagination (default: 1)
    """
    
    queryset = Todo.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_fields = ['completed', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'priority', 'due_date']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer based on action.
        
        - list: Use lightweight list serializer
        - retrieve: Use full serializer
        - partial_update: Use partial update serializer
        - create/update: Use full serializer
        """
        if self.action == 'list':
            return TodoListSerializer
        elif self.action == 'partial_update':
            return TodoPartialUpdateSerializer
        return TodoSerializer

    def list(self, request, *args, **kwargs):
        """List todos with filtering, searching, and pagination.
        
        Filters todos by query parameters:
        - completed: Filter by completion status (true/false)
        - priority: Filter by priority level (low/medium/high)
        - search: Search in title and description
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
            
            # Handle boolean filter for 'completed' parameter
            completed = request.query_params.get('completed')
            if completed is not None:
                # Convert string to boolean
                if completed.lower() in ['true', '1', 'yes']:
                    queryset = queryset.filter(completed=True)
                elif completed.lower() in ['false', '0', 'no']:
                    queryset = queryset.filter(completed=False)
                else:
                    raise ValidationError({"completed": "Must be 'true' or 'false'"})
            
            # Apply search if provided
            search = request.query_params.get('search')
            if search:
                queryset = queryset.filter(
                    Q(title__icontains=search) | Q(description__icontains=search)
                )
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                logger.info(f"Listed {len(page)} todos for user")
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            logger.info(f"Listed {queryset.count()} todos for user")
            return Response(serializer.data)
        
        except ValidationError as e:
            logger.warning(f"Validation error in list: {e}")
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error in list: {e}")
            return Response(
                {"error": "An unexpected error occurred while listing todos"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        """Create a new todo with validation.
        
        Request body:
        {
            "title": "string (required, max 255)",
            "description": "string (optional)",
            "priority": "low|medium|high (default: low)",
            "due_date": "ISO datetime (optional)",
            "completed": "boolean (default: false)"
        }
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            logger.info(f"Created todo: {serializer.data['id']}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logger.warning(f"Validation error in create: {e}")
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error in create: {e}")
            return Response(
                {"error": "An unexpected error occurred while creating todo"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific todo by ID."""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            logger.info(f"Retrieved todo: {instance.id}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving todo: {e}")
            return Response(
                {"error": "Todo not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, *args, **kwargs):
        """Full update of a todo (PUT request).
        
        All fields must be provided.
        """
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            logger.info(f"Updated todo: {instance.id}")
            return Response(serializer.data)
        except ValidationError as e:
            logger.warning(f"Validation error in update: {e}")
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error updating todo: {e}")
            return Response(
                {"error": "An unexpected error occurred while updating todo"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def partial_update(self, request, *args, **kwargs):
        """Partial update of a todo (PATCH request).
        
        Only provided fields are updated.
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete a todo."""
        try:
            instance = self.get_object()
            todo_id = instance.id
            self.perform_destroy(instance)
            logger.info(f"Deleted todo: {todo_id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting todo: {e}")
            return Response(
                {"error": "An unexpected error occurred while deleting todo"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def complete(self, request, pk=None):
        """Mark a todo as completed.
        
        PATCH /api/todos/{id}/complete/
        
        Response: {"status": "todo marked as completed"}
        """
        try:
            todo = self.get_object()
            todo.completed = True
            todo.save(update_fields=['completed', 'updated_at'])
            serializer = self.get_serializer(todo)
            logger.info(f"Marked todo as completed: {todo.id}")
            return Response(
                {"status": "todo marked as completed", "todo": serializer.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error completing todo: {e}")
            return Response(
                {"error": "An unexpected error occurred while completing todo"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def uncomplete(self, request, pk=None):
        """Mark a completed todo as incomplete.
        
        PATCH /api/todos/{id}/uncomplete/
        
        Response: {"status": "todo marked as incomplete"}
        """
        try:
            todo = self.get_object()
            todo.completed = False
            todo.save(update_fields=['completed', 'updated_at'])
            serializer = self.get_serializer(todo)
            logger.info(f"Marked todo as incomplete: {todo.id}")
            return Response(
                {"status": "todo marked as incomplete", "todo": serializer.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error uncompleting todo: {e}")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def perform_create(self, serializer):
        """Save a new todo instance."""
        serializer.save()

    def perform_update(self, serializer):
        """Save updated todo instance."""
        serializer.save()
