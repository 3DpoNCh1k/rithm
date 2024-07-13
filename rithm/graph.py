from graphlib import CycleError, TopologicalSorter


def has_cycle(graph):
    try:
        get_topological_order(graph)
        return False, []
    except CycleError as e:
        return True, e.args[1]


def get_topological_order(graph):
    return tuple(TopologicalSorter(graph).static_order())
