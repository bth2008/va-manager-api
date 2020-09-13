from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class APConfig(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'main:garbage_collection',
            'args': (),
            'trigger': 'interval',
            'seconds': 60
        }
    ]

    SCHEDULER_API_ENABLED = True
