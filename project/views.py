from rest_framework import generics

# projects/
class ProjectListCreateAPIView(generics.ListCreateAPIView):
    # queryset = Project.objects.filter(user in users)
    pass

# project/{id}
class ProjectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    pass
