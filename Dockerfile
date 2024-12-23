FROM nvcr.io/nvidia/pytorch:24.06-py3

WORKDIR /app

COPY requirement.txt .

RUN sed -i '/pywin32/d' requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
