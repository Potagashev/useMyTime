from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from report.constants import handle_required_fileds_were_not_provided
from timer.models import TaskTimer


class GetReportForPeriod(APIView):
    """<h2>Just provide start and end data in ISO format like '2022-01-01'</h2>"""
    def post(self, request):
        user = self.request.user
        try:
            start = self.request.data['start']
            end = self.request.data['end']
        except KeyError as err:
            return handle_required_fileds_were_not_provided(err.args)

        # протестить надо, как будет работать с активным таймером. то есть когда энд тайм не указан
        # и посмотреть, как он будет работать с анонимными тасками
        sessions = TaskTimer.objects.filter(start_time__gte=start, end_time__lte=end, task__assignee=user)

        total_time = sessions.latest('end_time').end_time - sessions[0].start_time

        report = {}
        for session in sessions:
            task = session.task

            if task.id in report:
                hours = (session.end_time - session.start_time).seconds / 3600
                percents = 100 * hours / (total_time.seconds / 3600)
                report[task.id]['hours'] += hours
                report[task.id]['percents'] += percents

            else:
                department = task.assignee.department
                employee = task.assignee.displayName
                hours = (session.end_time - session.start_time).seconds / 3600
                percents = 100 * hours / (total_time.seconds / 3600)
                direction_type = task.project.direction_type
                project_type = task.project.type
                order = task.project.order
                description = task.description

                row = {
                    "department": department,
                    "employee": employee,
                    "hours": hours,
                    "percents": percents,
                    "direction_type": direction_type,
                    "project_type": project_type,
                    "order": order,
                    "description": description
                }
                report[task.id] = row
            print("alright im working on it")

        return Response(data=report, status=200)
