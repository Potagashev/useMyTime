from django.shortcuts import render
from rest_framework.views import APIView


# class GetReportForPeriod(APIView):
#     def post(self, request):
#         user = self.request.user
#         start = self.request.data['start']
#         end = self.request.data['end']
#         hours =
#         for i in range(30):
#             row = {}
#             row['Отдел'] = user.department
#             row['Сотрудник'] = user.displayName
#             row['Часы'] = get_total_time_by task(task)
#             hours += row['Часы']
#             row['%'] = 100 * (row['Часы'] / get_total_time_for_period())
#             row['Б'] = task.project.direction_type
#             row['Тип'] = task.project.type
#             row['Заказ'] = task.project.order
#             row['Расшифровка'] = task.description
#
#         total_time = get_total_time_for_period(start, end)