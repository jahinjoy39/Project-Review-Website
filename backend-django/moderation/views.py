from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Report
from .serializers import ReportSerializer


class IsAdminUserRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().select_related(
        'reporter',
        'reviewed_by',
        'project'
    ).order_by('-created_at')
    serializer_class = ReportSerializer

    def get_permissions(self):
        if self.action in ['create', 'my_reports']:
            return [permissions.IsAuthenticated()]
        if self.action in ['list', 'retrieve', 'update_status']:
            return [IsAdminUserRole()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        status_param = self.request.query_params.get('status')
        target_type = self.request.query_params.get('target_type')

        if status_param:
            qs = qs.filter(status=status_param)
        if target_type:
            qs = qs.filter(target_type=target_type)

        return qs

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    @action(detail=False, methods=['get'])
    def my_reports(self, request):
        reports = Report.objects.filter(reporter=request.user).order_by('-created_at')
        return Response(self.get_serializer(reports, many=True).data)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        report = self.get_object()
        new_status = request.data.get('status')

        if new_status not in ['pending', 'reviewed', 'resolved', 'dismissed']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        report.status = new_status
        report.reviewed_by = request.user
        report.reviewed_at = timezone.now()
        report.save()

        return Response(self.get_serializer(report).data)