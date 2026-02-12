FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

COPY .env /app/

RUN python <<EOF
from transformers import pipeline

pipeline(
'text-classification',
model='SamLowe/roberta-base-go_emotions',
top_k=None
)
EOF

CMD ["python", "main.py"]