# Stage 1: builder
FROM python:3.11-slim AS builder
WORKDIR /build

# Install build tools
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and build wheels
COPY app/requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip wheel --wheel-dir=/wheels -r requirements.txt

# Stage 2: runtime
FROM python:3.11-slim
ENV TZ=UTC
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y cron tzdata && rm -rf /var/lib/apt/lists/*

# Copy wheels and requirements.txt from builder
COPY --from=builder /wheels /wheels
COPY --from=builder /build/requirements.txt /build/requirements.txt

# Install Python dependencies from wheels
RUN pip install --no-index --find-links=/wheels -r /build/requirements.txt

# Copy app code and cron jobs
COPY app /app
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# Copy PEM keys
COPY student_private.pem /app/student_private.pem
COPY student_public.pem /app/student_public.pem
COPY instructor_public.pem /app/instructor_public.pem

# Setup cron
RUN chmod 0644 /etc/cron.d/2fa-cron \
    && crontab /etc/cron.d/2fa-cron

# Create directories and set volumes
RUN mkdir -p /data /cron
VOLUME ["/data", "/cron"]

# Expose port and start services
EXPOSE 8080
CMD service cron start && uvicorn main:app --host 0.0.0.0 --port 8080
