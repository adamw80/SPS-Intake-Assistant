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

# Set the PATH to use the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Expose ports for Rasa server and Action server
EXPOSE 5005
EXPOSE 5060

# Install supervisord
RUN apt-get update && apt-get install -y supervisor

# Copy the supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start supervisord
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
