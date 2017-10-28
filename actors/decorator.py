import logging

log = logging.getLogger('thespian.log')


def log_arguments(method):
    """
    Class Method Wrapper for logging
    """

    def inner(actor_instance, message, sender):
        classname = actor_instance.__class__.__name__
        methodname = method.__name__.lstrip('receiveMsg_')
        msg = str(message)
        log.debug(f"{classname}[{methodname}] : {msg}")
    return inner
