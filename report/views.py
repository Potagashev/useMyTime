from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime

from report.constants import handle_required_fileds_were_not_provided, SESSIONS_NOT_FOUND_RESPONSE
from timer.models import TaskTimer


class GetReportForPeriod(APIView):
    """<h2>Just provide start and end data in ISO format like '2022-01-31'</h2>"""
    def post(self, request):
        user = self.request.user
        try:
            start = self.request.data['start']
            end = self.request.data['end']
        except KeyError as err:
            return handle_required_fileds_were_not_provided(err.args)

        start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end, '%Y-%m-%d') + datetime.timedelta(hours=23, minutes=59, seconds=59, microseconds=999999)

        sessions = TaskTimer.objects.filter(start_time__gte=start_date, end_time__lte=end_date, task__assignee=user)
        if sessions:
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
                    direction_type = task.project.direction_type.abbreviation
                    project_type = task.project.type.abbreviation
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
        else:
            return SESSIONS_NOT_FOUND_RESPONSE
