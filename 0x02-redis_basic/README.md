# 0x02. Redis basic
`Back-end` `Redis`

![Redis](https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/medias/2020/1/40eab4627f1bea7dfe5e.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20241023%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241023T071023Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=3efd5a6627368ce0e8e9dbea066898a85538635fd4ac416e2c52639a02614e6c)

## Resources
**Read or watch:**
* [Redis Crash Course Tutorial](https://www.youtube.com/watch?v=Hbt56gFj998)
* [Redis commands](https://redis.io/docs/latest/commands/)
* [Redis python client](https://redis-py.readthedocs.io/en/stable/)
* [How to Use Redis With Python](https://realpython.com/python-redis/)

## Learning Objectives
* Learn how to use redis for basic operations
* Learn how to use redis as a simple cache

## Install Redis on Ubuntu 18.04
```
$ sudo apt-get -y install redis-server
$ pip3 install redis
$ sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf
```

## Use Redis in a container
Redis server is stopped by default - when you are starting a container, you should start it with: `service redis-server start`
