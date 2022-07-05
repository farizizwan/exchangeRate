from redis_om import get_redis_connection

redis = get_redis_connection(
    host = "redis-12902.c273.us-east-1-2.ec2.cloud.redislabs.com",
    port = 12902,
    password = "pVjNe4Qu6ERA1S01x0Xx2FtQ50SYpmo3",
    decode_responses = True
)