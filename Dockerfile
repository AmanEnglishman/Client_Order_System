FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python3 -c "import sys; content = open('/app/entrypoint.sh', 'rb').read(); open('/app/entrypoint.sh', 'wb').write(content.replace(b'\r\n', b'\n').replace(b'\r', b'')); import os; os.chmod('/app/entrypoint.sh', 0o755)"

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "clientordersystem.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
