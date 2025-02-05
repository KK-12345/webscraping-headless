FROM python:3.12.3-slim
COPY . frontend/

WORKDIR /frontend

RUN pip install --no-cache-dir -r f_requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "ui_form.py"]
