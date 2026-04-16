FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend .
RUN npm run build

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .
COPY --from=frontend-builder /app/frontend/build /app/frontend/build
RUN mkdir -p /app/static /app/staticfiles /app/frontend/build && cp -r /app/frontend/build/static/. /app/staticfiles/
RUN python3 -c "import sys; content = open('/app/entrypoint.sh', 'rb').read(); open('/app/entrypoint.sh', 'wb').write(content.replace(b'\r\n', b'\n').replace(b'\r', b'')); import os; os.chmod('/app/entrypoint.sh', 0o755)"
EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "clientordersystem.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
