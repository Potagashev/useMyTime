from rest_framework.response import Response


def handle_required_fileds_were_not_provided(data: tuple):
    return Response(status=400, data={'details': f'You did not provide all data {data}'})


SESSIONS_NOT_FOUND_RESPONSE = Response(data={'details': 'There are no working sessions found. Make sure that the end '
                                                        'date is later than the start date. Probably, the timer was '
                                                        'not in use during this period.'}, status=418)
