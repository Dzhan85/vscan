# Multi-stage build for optimized image size
FROM python:3.11-slim AS builder

LABEL maintainer="RP2"
LABEL description="Virtual Host Scanner - Fast and efficient vhost discovery tool"

WORKDIR /build

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application files
COPY . .

# Install the application
RUN python setup.py install --user

# Final stage - minimal runtime image
FROM python:3.11-slim

WORKDIR /vscan

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /build /vscan

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Create non-root user for security
RUN useradd -m -u 1000 vscan && \
    chown -R vscan:vscan /vscan

USER vscan

ENTRYPOINT ["vscan"]
CMD ["--help"]

