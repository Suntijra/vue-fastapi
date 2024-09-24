FROM python:3.10
WORKDIR /backend
COPY . .
# ตั้งค่าตัวแปรสภาพแวดล้อม
ENV POETRY_VERSION=1.6.1
ENV POETRY_VIRTUALENVS_CREATE=false

# ติดตั้ง Dependencies สำหรับ Poetry และ Python
RUN apt-get update && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# เพิ่ม Poetry ไปยัง PATH
ENV PATH="/root/.local/bin:$PATH"


    
RUN poetry install --no-root --no-dev


EXPOSE 3030

CMD ["python", "main.py"]

