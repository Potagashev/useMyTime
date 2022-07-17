import json

from rest_framework.response import Response
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
