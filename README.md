# python-celery-demo

## Introduction

### 1. You have to create a virtual environment for this project
``` bash
python3 -m venv venv
```

### 2. Activate the virtual environment
``` bash
source venv/bin/activate
```

### 3. In the core/celery.py file, we create a celery instance
``` python
app = Celery('core', include=['core'])
```

### 4. In the core/celeryconfig.py file, we create a celery configuration
``` python
class Config:
    broker_url = 'redis://10.201.10.150:6379/0'
    result_backend = 'redis://10.201.10.150:6379/0'
    task_serializer = 'json'
    result_serializer = 'json'
```

### 5. we add this configuration to the celery instance
``` python
app.config_from_object(Config)
```

### 6. We create a task to run **print(hello world)**
``` python
@app.task(name='tasks.test')
def test():
    print("hello world")
```

### 7. We add periodic task configuration to the celery instance
``` python
app.conf.beat_schedule = {
    "execute-every-minute": {
        "task": "tasks.test",
        # every day at midnight
        "schedule": crontab(minute=0, hour=0)
    }
}
```

## Docker configuration

### 1. We create a Dockerfile.worker file for celery worker
``` dockerfile
FROM python:3.10

ADD . /app/
WORKDIR /app/
RUN pip install -r requirements.txt
CMD ["celery", "-A", "core.celery", "worker", "-l", "INFO"]
```

### 2. We create a Dockerfile.beat file for celery beat
``` dockerfile
FROM python:3.10

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["celery", "-A", "core.celery", "beat", "-l", "INFO"]
```

### 3. We create a docker-compose.yml file for build containers
``` yaml
version: '3'
services:
  redis:
    image: redis
    ports:
    - "6379:6379"
  beat:
    build:
      context: .
      dockerfile: ./Dockerfile.beat
    volumes:
    - ./:/app/
    depends_on:
      - redis
  worker:
   build:
     context: .
     dockerfile: ./Dockerfile.worker
   volumes:
   - ./:/app/
   depends_on:
     - redis
```

### 4. We build containers
``` bash
docker-compose build
```

*Happy coding...*
====================================
