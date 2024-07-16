import os
import io
from dotenv import load_dotenv
from PIL import Image
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import ImageCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeImageOptions, ImageData

load_dotenv()

key = os.getenv('AZURE_KEY')
endpoint = os.getenv('AZURE_END_POINT')

    # Create a Content Safety client
client = ContentSafetyClient(endpoint, AzureKeyCredential(key))


def azure_predict_image(image_file):
    # input_image = Image.open(image_file)
    # image_bytes = image_file.read()
    # width, height = input_image.size
    # max_dimension = 2048
    # # Kiểm tra nếu một trong hai chiều vượt quá giới hạn
    # if width > max_dimension or height > max_dimension:
    #     # Tính toán tỷ lệ thay đổi kích thước
    #     if width > height:
    #         ratio = max_dimension / float(width)
    #         new_width = max_dimension
    #         new_height = int((float(height) * float(ratio)))
    #     else:
    #         ratio = max_dimension / float(height)
    #         new_width = int((float(width) * float(ratio)))
    #         new_height = max_dimension

    #         # Thay đổi kích thước ảnh
    #     input_image = input_image.resize((new_width, new_height), Image.ANTIALIAS)

    #     # Convert image to bytes for Azure request
    #     try:
    #         image_bytes = io.BytesIO()
    #         input_image.save(image_bytes, format='PNG')
    #         image_bytes = image_bytes.getvalue()
    #     except Exception as e:
    #         raise ValueError(f"Could not convert image to bytes: {e}")
    # Build request
    request = AnalyzeImageOptions(image=ImageData(content=image_file.read()))

    # Analyze image
    try:
        response = client.analyze_image(request)
    except HttpResponseError as e:
        print("Analyze image failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise

    sexual_result = next(item for item in response.categories_analysis if item.category == ImageCategory.SEXUAL)

    if sexual_result:
        return sexual_result.severity
    return 0