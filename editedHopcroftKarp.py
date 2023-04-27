# Source: https://networkx.org/documentation/stable/_modules/networkx/algorithms/bipartite/matching.html#hopcroft_karp_matching
import collections

from networkx.algorithms.bipartite import sets as bipartite_sets

INFINITY = float("inf")

def availabilityMatching(G, top_nodes=None):

    """Returns the maximum cardinality matching of the bipartite graph `G`.

    A matching is a set of edges that do not share any nodes. A maximum
    cardinality matching is a matching with the most edges possible. It
    is not always unique. Finding a matching in a bipartite graph can be
    treated as a networkx flow problem.

    The functions ``hopcroft_karp_matching`` and ``maximum_matching``
    are aliases of the same function.

    Parameters
    ----------
    G : NetworkX graph

      Undirected bipartite graph

    top_nodes : container of nodes

      Container with all nodes in one bipartite node set. If not supplied
      it will be computed. But if more than one solution exists an exception
      will be raised.

    Returns
    -------
    matches : dictionary

      The matching is returned as a dictionary, `matches`, such that
      ``matches[v] == w`` if node `v` is matched to node `w`. Unmatched
      nodes do not occur as a key in `matches`.

    Raises
    ------
    AmbiguousSolution
      Raised if the input bipartite graph is disconnected and no container
      with all nodes in one bipartite set is provided. When determining
      the nodes in each bipartite set more than one valid solution is
      possible if the input graph is disconnected.

    Notes
    -----
    This function is implemented with the `Hopcroft--Karp matching algorithm
    <https://en.wikipedia.org/wiki/Hopcroft%E2%80%93Karp_algorithm>`_ for
    bipartite graphs.

    See :mod:`bipartite documentation <networkx.algorithms.bipartite>`
    for further details on how bipartite graphs are handled in NetworkX.

    See Also
    --------
    maximum_matching
    hopcroft_karp_matching
    eppstein_matching

    References
    ----------
    .. [1] John E. Hopcroft and Richard M. Karp. "An n^{5 / 2} Algorithm for
       Maximum Matchings in Bipartite Graphs" In: **SIAM Journal of Computing**
       2.4 (1973), pp. 225--231. <https://doi.org/10.1137/0202019>.

    """
    
    def breadth_first_search():
        for v in staffNodes:
            #if this staff node has no identified matches yet, we add it to the 'distances' dictionary with a value of 0
            #this staff node (object?) then gets appended to the 'queue'.
            if staffMatches[v] is None:
                distances[v] = 0
                queue.append(v)
            #However, when the value of this staff in the staffMatches dictionary is not None (presume this means there is a match for this staff?),
            #we set this staff's value in the 'distances' dictionary to INFINITY.
                # My question so far, what is this 'distances' dictionary?
                # What is it tracking the state of? Distance from this staff node to what?
            else:
                distances[v] = INFINITY
        distances[None] = INFINITY
        while queue:
            v = queue.popleft()
            if distances[v] < distances[None]:
                for u in G[v]:
                    if distances[roleMatches[u]] is INFINITY:
                        distances[roleMatches[u]] = distances[v] + 1
                        queue.append(roleMatches[u])
        return distances[None] is not INFINITY

    def depth_first_search(v):
        if v is not None:
            for u in G[v]:
                if distances[roleMatches[u]] == distances[v] + 1:
                    if depth_first_search(roleMatches[u]):
                        roleMatches[u] = v
                        staffMatches[v] = u
                        return True
            distances[v] = INFINITY
            return None
        return True

    # Initialize the "global" variables that maintain state during the search.
    staffNodes, roleNodes = bipartite_sets(G, top_nodes)
    staffMatches = {v: None for v in staffNodes}
    roleMatches = {v: None for v in roleNodes}
    distances = {}
    queue = collections.deque()

    # Implementation note: this counter is incremented as pairs are matched but
    # it is currently not used elsewhere in the computation.
    num_matched_pairs = 0
    while breadth_first_search():
        for v in staffNodes:
            if staffMatches[v] is None:
                if depth_first_search(v):
                    num_matched_pairs += 1

    return roleMatches