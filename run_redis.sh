docker run \
    --name redis-deduplicator-server \
    -e REDIS_ARGS="--save 60 1000 --appendonly yes"\
    -d \
    -p 6379:6379 \
    -v ${PWD}/data/:/data redis/redis-stack:latest
