# Base image for Rasa
FROM rasa/rasa:3.1.0

# Set working directory for the Rasa app
WORKDIR /app

# Copy all files from the repository to the container
COPY . /app

# Install dependencies without upgrading pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for Rasa server and Action server
EXPOSE 5005
EXPOSE 5060

# Start both Rasa server and Action server
CMD ["bash", "-c", "rasa run --enable-api --cors '*' & rasa run actions --port 5060"]
