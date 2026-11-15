import networkx as nx
from django.db.models import Exists

from network.models import Edge, Node


def shortest_path(source, destination):
    """
    Return (total_latency, path) of the cheapest route, or None if no route.
    The same source and destination gives (0.0, [source]).
    """
    if source == destination:
        return 0.0, [source]

    # Fail fast in one query: nothing leaves the source or nothing enters the
    # destination.
    has_out, has_in = (
        Node.objects.filter(name=source)
        .annotate(
            has_out=Exists(Edge.objects.filter(source__name=source)),
            has_in=Exists(Edge.objects.filter(destination__name=destination)),
        )
        .values_list("has_out", "has_in")
        .get()
    )
    if not (has_out and has_in):
        return None

    graph = nx.DiGraph()
    edges = Edge.objects.values_list("source__name", "destination__name", "latency")
    graph.add_weighted_edges_from(edges)
    try:
        total_latency, path = nx.single_source_dijkstra(graph, source, destination)
    except nx.NetworkXNoPath:
        return None
    return round(float(total_latency), 4), path
