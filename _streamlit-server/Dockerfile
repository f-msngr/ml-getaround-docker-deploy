# Lightweight base image
FROM python:3.11-slim

ARG PORT_STREAMLIT_EXPOSED
ENV PORT_STREAMLIT_EXPOSED=${PORT_STREAMLIT_EXPOSED}

ENV PYTHONPATH="/app/streamlit:/app"

# Install system dependencies
# RUN apt-get update && apt-get install -y \
#    curl \
#    lsof \
#    net-tools \
#    procps \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy necessary files into the image
# In local development, this will be overwritten by a volume mount
# Explicitly create the working directory
# so it can be referenced in the WORKDIR directive
# because the 'streamlit' volume is bind-mounted via docker-compose
RUN mkdir -p /app/streamlit

# Copy configuration files
COPY ./_streamlit-server/requirements.txt .
# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Streamlit port
EXPOSE $PORT_STREAMLIT_EXPOSED

# Allow /app/pipeline to be imported as python module
# pipeline mounted as volume in docker-compose.yml
ENV PYTHONPATH="/app/pipeline:${PYTHONPATH}"

# Set 'streamlit' as the working directory
WORKDIR /app/streamlit
# Launch Streamlit
CMD ["sh", "-c", "streamlit run src/streamlit.py --server.address=0.0.0.0 --server.port=$PORT_STREAMLIT_EXPOSED --server.baseUrlPath=/dashboard"]