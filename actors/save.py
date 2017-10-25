from thespian.actors import ActorTypeDispatcher, ActorExitRequest


class SaveActor(ActorTypeDispatcher):
    """
    Save Method
    """

    def __init__(self):
        super().__init__()
        