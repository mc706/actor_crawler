from thespian.actors import ActorSystem

from actors.suite import SuiteActor
from actors.messages import SiteRequestMsg


def start_suite(name: str = None) -> None:
    """
    Starts the suite
    """
    print('start_suite', name)
    system = ActorSystem('multiprocTCPBase', {'Admin Port': 1900})
    actor = system.createActor(SuiteActor, globalName='suite')
    message = SiteRequestMsg(name[0])
    system.tell(actor, message)

if __name__ == "__main__":
    import sys

    start_suite(sys.argv[1:])