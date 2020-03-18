from os import environ as env


broker_url = env.get('BROKER_URL', 'amqp://rabbitmq:rabbitmq@localhost:5672')
result_backend = env.get('BACKEND_URL', 'redis://localhost/2')

task_create_missing_queues = True
result_expires = 60 * 60 * 3  # 3 hours
result_chord_join_timeout = 120
task_acks_late = True
task_reject_on_worker_lost = True
task_serializer = 'json'
task_default_queue = 'destiny'
