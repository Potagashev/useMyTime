import io
import json

from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from project.constants import MIN_PRIORITY, MAX_PRIORITY
from project.models import Task, Project
from user.models import User


def validate_members(user_id: int, members: list) -> list:
    """ описываю валидацию подчиненных
    если переданные подчиненные - реально подчиненные - ок,
    если нет - игнорим их """
    validated_members = []
    if members:
        for member_id in members:
            if User.objects.get(id=member_id).manager.id == user_id:
                validated_members.append(member_id)

    return validated_members


def create_task(request) -> Task:
    data = json.loads(request.body)
    project = Project.objects.get(id=data['project'])

    # если проект принадлежит тому, что делал запрос, то задача назначается тому,
    # кому указано
    if request.user.id == project.owner:
        assignee_id = User.objects.get(data['assignee']).id
    # если проект чужой, то задача назначается текущему юзеру
    else:
        assignee_id = request.user.id

    task = Task.objects.create(
        name=data['name'],
        description=data['description'],
        project=project,
        assignee=User.objects.get(id=assignee_id),
        deadline=data['deadline']
    )
    return task


def validate_data_for_project_creating(request):
    stream = io.BytesIO(request.body)
    data = JSONParser().parse(stream)

    try:
        priority = data['priority']
        if priority < MIN_PRIORITY or priority > MAX_PRIORITY:
            return Response({'details': f'priority should be >={MIN_PRIORITY} or <={MAX_PRIORITY}'})
    except KeyError:
        pass

    try:
        members = data['users']
    except KeyError:
        members = []
    validated_members = validate_members(user_id=request.user.id, members=members)
    validated_members.append(request.user.id)

    data['users'] = validated_members
    data['owner'] = request.user.id

    return data
