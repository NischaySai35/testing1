FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# pull in every published OS fix
RUN apk upgrade --no-cache

# install the app's libraries, then remove the installers: pip / setuptools are not needed
# at runtime and are the usual source of CVEs in Python images
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && pip uninstall -y setuptools wheel \
 && python -m pip uninstall -y pip

COPY app.py .
COPY templates templates
COPY static static

# never run as root
RUN adduser -D -u 10001 app
USER app

EXPOSE 8000
CMD ["python", "app.py"]
