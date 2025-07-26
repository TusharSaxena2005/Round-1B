FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (minimal for CPU-only operation)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py ./
COPY approach_explanation.md ./

# Create input and output directories
RUN mkdir -p /app/Input/PDFs /app/Output

# Set environment variables for optimization
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command shows usage
CMD ["python", "run_example.py"]

# Alternative entrypoint for direct execution
# ENTRYPOINT ["python", "main.py"]
