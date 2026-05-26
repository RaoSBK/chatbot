# Multi-stage production build for ml-engine
FROM python:3.10-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
# Since ml-engine has no requirements.txt, install basic dependencies directly
RUN pip install --no-cache-dir --user numpy pandas scikit-learn

FROM python:3.10-slim AS runner
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8001
# Run a simple python script/service or mock command depending on how it's structured.
# Since it does not contain a FastAPI app by default, we can run a placeholder loop to keep the container alive.
CMD ["python", "-c", "import time; print('ML Engine service started...'); [time.sleep(3600) for _ in iter(int, 1)]"]
