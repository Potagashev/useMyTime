from rest_framework.response import Response


def handle_required_fileds_were_not_provided(data: tuple):
    return Response(status=400, data={'details': f'You did not provide all data {data}'})
