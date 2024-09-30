from rest_framework import viewsets, mixins, serializers, status
from file.serializers import IndividualInformationSerializer
from utils.factory_parse_data import create_new_data
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class CreateIndividualInfoViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = IndividualInformationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        insurer = request.query_params.get("insurer")
        if insurer is None:
            raise serializers.ValidationError(
                "Please enter insurance name from query params!"
            )

        data = request.data.copy()
        correct_data = create_new_data(insurer=insurer, data=data)
        if not correct_data:
            raise serializers.ValidationError("Your insurer is not valid.")
        serializer = IndividualInformationSerializer(
            data=correct_data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
