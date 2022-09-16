from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from report.constants import you_didnt_provide_all_data_response


class GetReportForPeriod(APIView):
    def post(self, request):
        user = self.request.user
        try:
            start = self.request.data['start']
            end = self.request.data['end']
        except KeyError as err:
            return you_didnt_provide_all_data_response(err.args)

        start_date = datetime.strptime(start, '%Y-%m-%d').date()
        end_date = datetime.strptime(end, '%Y-%m-%d').date()
        print((end_date - start_date).days)

        response = Response()
        return response
        # for i in range(30):
        #     row = {}
        #     row['Отдел'] = user.department
        #     row['Сотрудник'] = user.displayName
        #     row['Часы'] = get_total_time_by task(task)
        #     hours += row['Часы']
        #     row['%'] = 100 * (row['Часы'] / get_total_time_for_period())
        #     row['Б'] = task.project.direction_type
        #     row['Тип'] = task.project.type
        #     row['Заказ'] = task.project.order
        #     row['Расшифровка'] = task.description
        #
        # total_time = get_total_time_for_period(start, end)