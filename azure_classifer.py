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

def resize_image(image_data, max_size=(2048, 2048)):
    # Mở hình ảnh từ dữ liệu binary
    image = Image.open(io.BytesIO(image_data))
    
    # Giảm kích thước hình ảnh
    image.thumbnail(max_size, Image.ANTIALIAS)
    
    # Lưu hình ảnh đã thay đổi kích thước vào buffer
    buffer = io.BytesIO()
    image.save(buffer, format=image.format)
    buffer.seek(0)
    
    return buffer

def azure_predict_image(image_file):

    image_data = image_file.read()
    resized_image_buffer = resize_image(image_data)

    request = AnalyzeImageOptions(image=ImageData(content=resized_image_buffer.read()))

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