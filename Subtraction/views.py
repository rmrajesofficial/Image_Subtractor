from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProjectDocument
import cv2
import numpy as np
from django.core.files.base import ContentFile

class SubtractImagesAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
            first_image = cv2.imdecode(np.frombuffer(image1.read(), np.uint8), cv2.IMREAD_COLOR)
            second_image = cv2.imdecode(np.frombuffer(image2.read(), np.uint8), cv2.IMREAD_COLOR)
            subtracted = cv2.subtract(second_image,first_image)
            _, buffer = cv2.imencode('.jpg', subtracted)
            subtracted_image_file = ContentFile(buffer.tobytes())
            project_document = ProjectDocument()
            project_document.file.save('subtracted_image.jpg', subtracted_image_file)
            project_document.save()
            response_data = {
                'file_field': {
                    'url': project_document.file.url,
                    'name': project_document.file.name,
                    'size': project_document.file.size,
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except cv2.error as cv2_error:
            error_message = f"OpenCV error: {str(cv2_error)}"
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
