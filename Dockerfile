# Sử dụng hình ảnh cơ sở của Python
FROM python:3.10.4-slim

# Cài đặt các thư viện hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép các file yêu cầu vào thư mục làm việc
COPY requirements.txt requirements.txt

# Cài đặt các thư viện Python yêu cầu
RUN pip install -r requirements.txt

# Sao chép toàn bộ mã nguồn vào thư mục làm việc
COPY . .

# Chạy ứng dụng với Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
