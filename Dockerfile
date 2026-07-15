FROM python:3.12-slim
RUN apt-get update && apt-get install -y \
tk \
x11-apps \
&& rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 1000 appuser
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=appuser:appuser . .
RUN mkdir -p /app/data && chown -R appuser:appuser /app/data
USER appuser
ENTRYPOINT ["python", "-m", "src.main"]
CMD ["--input", "data/sample_input.json"]
