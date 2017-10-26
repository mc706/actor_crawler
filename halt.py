from thespian.actors import ActorSystem, ActorExitRequest

from actors.suite import SuiteActor


def halt_suite():
    """
    Halts a running suite
    """
    print('halt_suite')
    system = ActorSystem('multiprocTCPBase', {'Admin Port': 1900})
    actor = system.createActor(SuiteActor, globalName='suite')
    system.tell(actor, ActorExitRequest())

if __name__ == "__main__":
    halt_suite()