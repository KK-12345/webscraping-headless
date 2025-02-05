FROM python:3.12.3-slim
COPY . backend/

WORKDIR /backend

RUN pip install --no-cache-dir -r b_requirements.txt
RUN python3 -m playwright install && playwright install-deps

EXPOSE 8000

CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
