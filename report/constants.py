from rest_framework.response import Response


def you_didnt_provide_all_data_response(data: tuple):
    return Response(status=400, data={'details': f'You did not provide all data {data}'})
