# coding=utf-8


from listenbrainz.listenstore import ListenStore, MIN_ID
import logging
import ujson
import uuid
from listenbrainz.listen import Listen
from redis import Redis
import redis
import json


class RedisListenStore(ListenStore):
    def __init__(self, conf):
        ListenStore.__init__(self, conf)
        self.log.info('Connecting to redis: %s:%s', conf['REDIS_HOST'], conf['REDIS_PORT'])
        self.redis = Redis(host=conf['REDIS_HOST'], port=conf['REDIS_PORT'], decode_responses=True)

    def get_playing_now(self, user_id):
        """ Return the current playing song of the user """
        data = self.redis.get('playing_now' + ':' + str(user_id))
        if not data:
            return None
        data = ujson.loads(data)
        data.update({'listened_at': MIN_ID+1})
        return Listen.from_json(data)

    def check_connection(self):
        """ Pings the redis server to check if the connection works or not """
        try:
            self.redis.ping()
        except redis.exceptions.ConnectionError as e:
            self.log.error("Redis ping didn't work: {}".format(str(e)))
            raise
