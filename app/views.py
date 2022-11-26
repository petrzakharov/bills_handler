from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Bill, Client, Organisation, Service
from app.serializers import BillUploadSerializer, BillViewSerializer
from app.utils import create_or_get_unique_db, file_prepare


class BillUploadView(APIView):
    http_method_names = ["post"]
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = BillUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        df = file_prepare(serializer.validated_data["file"])
        df_raw = list(df.T.to_dict().values())
        db_objects = {}
        for model, column_name in {
            Client: "client",
            Organisation: "organisation",
            Service: "service",
        }.items():
            db_objects[column_name] = create_or_get_unique_db(
                model=model, values=list(df[column_name].unique())
            )
        for record in df_raw:
            file = Bill(
                client=db_objects["client"][record["client"]],
                organisation=db_objects["organisation"][record["organisation"]],
                bill_number=record["bill_number"],
                summa=record["summa"],
                date=record["date"],
                service=db_objects["service"][record["service"]],
            )
            file.save()

        return Response({"status": "success"}, status.HTTP_201_CREATED)


class BillReadView(generics.ListAPIView):
    serializer_class = BillViewSerializer
    model = Bill
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('organisation__name', 'client__name')
    queryset = Bill.objects.all()

