FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime

ENV HF_TOKEN=""

WORKDIR /app

RUN apt-get update && apt-get install -y git build-essential gfortran ffmpeg && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt uv
RUN sed -i 's/compute_type = "float16"/compute_type = "int8" if device == "cpu" else "float16"/g' /opt/conda/lib/python*/site-packages/tribev2/eventstransforms.py

COPY . .

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
