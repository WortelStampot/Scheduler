# Source: https://networkx.org/documentation/stable/_modules/networkx/algorithms/bipartite/matching.html#hopcroft_karp_matching
import collections

from networkx.algorithms.bipartite import sets as bipartite_sets

INFINITY = float("inf")

def availabilityMatching(Graph, top_nodes=None):

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
        for staff in staffNodes:
            if staffMatches[staff] is None:
                distances[staff] = 0
                queue.append(staff) # What is this 'distances' dictionary tracking the state of?
            else:
                distances[staff] = INFINITY
        distances[None] = INFINITY 
        while queue: #this loop checks if there is a staff node in the set, for whom to identify a connecting edge (this will be done with the depth-first-search). 
            staff = queue.popleft()
            if distances[staff] < distances[None]:
                debugGraph = Graph[staff]
                for role in Graph[staff]: # In this loop we go through each role this staff is connected (adjacent?) to.
                    #the staff node being the dictionary key to get into a deeper dictionary of the graph data strucutre. A dictionary of connected role nodes for each staff.
                    if distances[roleMatches[role]] is INFINITY: # when the value of roleMatches[role] is None, this expression evaluates to: distances[None]
                        #this means there is yet to be a match for this role.
                        #And this is what the None node above has been established for?
                        #since now this expression returns True as distances[None] is INFINITY?
                        distances[roleMatches[role]] = distances[staff] + 1 # now we incremint the distance value of the None node by the distance value of the staff Node (0) + 1.
                        #what happens is this sets the None node value from inf to 1.
                        #this is important since flipping the None node from inf to 1 informs us 'hey, there is a staff and role node in these sets for whom to perform a depth first search'

        return distances[None] is not INFINITY #returning True now that distances[None] is 1 (not INFINITY).
    #this saying, True- there are at least one staff and role nodes in these two sets 'unchecked' for a match.
    #which translates to saying True- it makes sense to go on and perform the depth first search.

    def depth_first_search(staff): #At this point we have identified this is a staff whom to do a search for.
        if staff is not None:
            for role in Graph[staff]: #for each role this staff is connected to.
                if distances[roleMatches[role]] == distances[staff] + 1: #when the value of None node is 1 and value of staff distance is 0, this returns True. 
                    if depth_first_search(roleMatches[role]): #if this role also doesn't have a match yet,
                        roleMatches[role] = staff #this staff is set as a match with this role
                        staffMatches[staff] = role #this role is set to match with this staff
                        #In other words, this confirms an edge exists between the the role and staff node which has been established earlier.
                        #So a 'match' is actually the first occuring edge between an 'open' (yet unmatched) role and staff node in the graph?
                        return True #and returning True, takes us out of the function, allows us to increment the num_matched_pairs counter, and go through these steps again with the following staff.
                    
            distances[staff] = INFINITY #when going through all the connected roles of a staff, and there is no corosponding 'open' connected role, we hit this expression
            return None #and return None.
        return True #this line is hit when the staff variable is 'None'?
    #When would there be a 'None' node in the staffNodes list?

    # Initialize the "global" variables that maintain state during the search.
    staffNodes, roleNodes = bipartite_sets(Graph, top_nodes)
    staffMatches = {staff: None for staff in staffNodes}
    roleMatches = {role: None for role in roleNodes}
    distances = {} # What this dictionary represents is still fuzzy to me.
    queue = collections.deque()

    # Implementation note: this counter is incremented as pairs are matched but
    # it is currently not used elsewhere in the computation.
    num_matched_pairs = 0
    while breadth_first_search(): #while there are at least one staff and role node in the two sets 'unchecked' for a match.
        # rephrasing: while distances[None] is not INFINITY
        #This is the 'breadth' part of the search. Checking a surface 'True/False' across the two sets of node, for whether to continue searching.
        #This is also why the staff nodes need to be unique objects? Since each staff object (node) gets its own distance value?

        for staff in staffNodes: #go through each staff node in the staff node set.
            if staffMatches[staff] is None: # This statement culls from a 'yes there is a staff for whom to perform the deeper search for in the set,
                #down to 'this is the staff for whom to perform a depth first search for.'
                if depth_first_search(staff): #This statement is True when a depth first search results in identifing a match with this staff to a role node.
                    #this depth first search function also 'sets' the match value (when a match is found) in the staffMatches/roleMatches dictionaries.
                    num_matched_pairs += 1

    return roleMatches