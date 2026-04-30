# Start from official Python 3.12 slim image (smaller than full image)
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency file first — layer caching means this step is
# skipped on rebuild if pyproject.toml hasn't changed
COPY pyproject.toml .

# Install dependencies
RUN uv sync

# Copy application code (changes more often than dependencies)
COPY module-00-foundations/backend-basics/main.py .

# Run uvicorn bound to 0.0.0.0 so it's reachable outside the container
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
