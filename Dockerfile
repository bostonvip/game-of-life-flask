FROM python:3.12-slim

# Add a non-root user and establish dependencies
RUN useradd -m -r service && \
    mkdir /app && \
    chown -R service:service /app && \
    python -m pip install -U pip wheel

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source files
COPY --chown=service:service . .

USER service

# Run the service on port 8000
ENV PORT=8000
EXPOSE $PORT
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
