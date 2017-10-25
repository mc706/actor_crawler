import logging

from thespian.actors import ActorSystem


class actorLogFilter(logging.Filter):
    def filter(self, logrecord):
        return 'actorAddress' in logrecord.__dict__


class notActorLogFilter(logging.Filter):
    def filter(self, logrecord):
        return 'actorAddress' not in logrecord.__dict__


logcfg = {
    'version': 1,
    'formatters': {

        'normal': {
            'format': '%(levelname)-8s %(message)s'
        },
        'actor': {
            'format': '%(levelname)-8s %(actorAddress)s => %(message)s'
        }
    },
    'filters': {
        'isActorLog': {
            '()': actorLogFilter
        },
        'notActorLog': {
            '()': notActorLogFilter
        }
    },
    'handlers': {
        'h1': {
            'class': 'logging.FileHandler',
            'filename': 'thespian.log',
            'formatter': 'normal',
            'filters': ['notActorLog'],
            'level': logging.INFO
        },
        'h2': {
            'class': 'logging.FileHandler',
            'filename': 'thespian.log',
            'formatter': 'actor',
            'filters': ['isActorLog'],
            'level': logging.INFO
        },
    },
    'loggers': {
        '': {
            'handlers': ['h1', 'h2'],
            'level': logging.DEBUG
        }
    }
}

capabilities = {
    'Admin Port': 1900,
    'Convention Address.IPv4': ('', 1900)
}

actsys = ActorSystem('multiprocTCPBase', capabilities=capabilities, logDefs=logcfg)
