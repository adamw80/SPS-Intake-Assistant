# Base image for Rasa
FROM rasa/rasa:3.0.0

# Set working directory
WORKDIR /app

# Copy Rasa project files
COPY . /app

# Install additional dependencies for actions
WORKDIR /app/actions
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for Rasa server and Action server
EXPOSE 5005
EXPOSE 5060

# Start both servers
CMD ["bash", "-c", "rasa run --enable-api --cors '*' & rasa run actions --port 5060"]
