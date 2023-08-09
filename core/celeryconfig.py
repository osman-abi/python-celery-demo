
class Config:
    broker_url = 'redis://10.201.10.150:6379/0'
    result_backend = 'redis://10.201.10.150:6379/0'
    task_serializer = 'json'
    result_serializer = 'json'
