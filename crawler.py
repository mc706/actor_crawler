from thespian.actors import ActorSystem

from actors.suite import SuiteActor
from actors.messages import SiteRequestMsg
from actors.log_config import logcfg

def start_suite(name: str = None) -> None:
    """
    Starts the suite
    """
    print('start_suite', name)
    system = ActorSystem('multiprocTCPBase', {'Admin Port': 1900, 'Convention Address.IPv4': ('', 1900)}, logDefs=logcfg)
    actor = system.createActor(SuiteActor, globalName='suite')
    message = SiteRequestMsg(name[0])
    system.ask(actor, message)
    system.shutdown()

if __name__ == "__main__":
    import sys
    start_suite(sys.argv[1:])