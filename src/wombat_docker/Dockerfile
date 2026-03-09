#
# docker build -t hyena:latest .
# docker run -v /var/wombat:/mnt/wombat --name hyena hyena:latest
# docker run -e stuntbox=score -v /var/wombat:/mnt/wombat --name hyena hyena:latest
# docker run -e stuntbox=score -e limit=5 -v /var/wombat:/mnt/wombat --name hyena hyena:latest
#
FROM python:3.11-slim

WORKDIR /app

# Create and activate virtualenv first
RUN python -m venv /app/venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements and install them inside the venv
COPY requirements.txt ./
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir -r requirements.txt

COPY hyena_app.py ./

RUN mkdir -p /mnt/wombat
CMD ["python", "hyena_app.py"]
