FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    libspatialite-dev \
    libgeos-dev \
    postgresql-client \
    gcc \
    python3-dev \
    git \
    build-essential \
    netcat-traditional \
    gettext \
    libmagic-dev \
    curl \
    sed \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set up virtual environment
RUN python -m venv $VIRTUAL_ENV

# Copy requirements first for better layer caching
COPY requirements/ /app/requirements/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements/dev.txt

# Copy project files
COPY . /app/

# Setup entrypoint and scripts
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
COPY docker/scripts/ /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh \
    && chmod +x /usr/local/bin/docker-*.sh

ENTRYPOINT ["entrypoint.sh"]

# Run development server by default
CMD ["python", "manage.py", "runserver", "0.0.0.0:8003"]