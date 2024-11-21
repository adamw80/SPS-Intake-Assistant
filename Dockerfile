# Base image for Rasa
FROM rasa/rasa:3.1.0

# Set working directory for the Rasa app
WORKDIR /app

# Copy all files from the repository to the container
COPY . /app

# Create a virtual environment
RUN python -m venv /app/venv

# Activate the virtual environment and install dependencies
RUN /app/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /app/venv/bin/pip install --no-cache-dir websockets==10.4 && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Switch to root to install supervisor
USER root
RUN apt-get update && apt-get install -y supervisor

# Create log directory with correct permissions
RUN mkdir -p /app/logs && chown 1001:1001 /app/logs

# Switch back to non-root user
USER 1001

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports for Rasa server and Action server
EXPOSE 5005
EXPOSE 5060

# Start Supervisor to run Rasa services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

