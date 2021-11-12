import math
import numpy as np
import scipy.sparse as sp
from collections import Counter
from scipy.sparse.csgraph import connected_components
from numba import njit


@njit
def lonlatdist(lon1, lat1, lon2, lat2):
    """calculate geodesic distance on sphere in kilometers, using a variant of
    the Haversine formula, copied from https://stackoverflow.com/a/38187562"""
    lon1, lat1 = lon1, lat1
    lon2, lat2 = lon2, lat2
    radius = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    if (1 - a) < 1e-9:
    	return (math.pi * radius)
    great_circle_distance = radius * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))  # in km
    return great_circle_distance


@njit
def get_D(lats=None, lons=None):
    """get distance matrix given lats and lons"""
    N = lats.size
    nodes = np.arange(N)
    D = np.zeros((N, N))
    for i in nodes:
        for j in nodes[:i]:
            D[i, j] = D[j, i] = lonlatdist(lons[i], lats[i], lons[j], lats[j])
    return D


def generate_links(N=None, lats=None, lons=None, D=None, M=None,
                   r0=1.0, gamma=2.0, make_connected=True):
    """Generate M links between the nodes given by either lats and lons or by
    a distance matrix d, using the following model:
    M times draw a node i. Find a partner j with relative probabilities
        1 / (1 + d(i,j)/r0)**gamma,
    where d(i,j) is the geodesic distance between i and j.
    The resulting mean degree is 2M/N and almost all nodes have degree >=M/N.
    If make_connected==True, finally make sure the network is connected by
    connecting a random node from each non-giant component to the closest node
    from the giant component. This increases the mean degree very slightly.

    @arg lats: (optional) array of node latitudes in degrees
    @arg lons: (optional) array of node longitudes in degrees
    @arg D: (optional) distance matrix in km

    Either lats and lons, or D must be given.

    @arg M: number of edges to generate
    @arg r0: characteristic distance in km, default: 1.0
    @arg gamma: decay exponent for linking probability, default: 2.0
    @arg make_connected: whether to make the network connected, default: True

    @return A, L: adjacency matrix and corresponding link lengths
                  as two scipy.sparse.lil_matrix

    Rationale for defaults: r0=1.0 makes sure the link length distribution
    starts decaying early, gamma=2.0 makes sure that for a uniform distribution
    of nodes, the link length distribution would look similar to
    Goldenberg & Levy 2009.
    """

    if D is not None:
        N = D.shape[0]
    else:
        N = lats.size
        D = get_D(lats=lats, lons=lons)

    nodes = np.arange(N)  # lil_matrix = This is a structure for constructing sparse matrices incrementally
    A = sp.lil_matrix((N, N), dtype=type(1))  # adjacency
    L = sp.lil_matrix((N, N), dtype=type(1.0))  # corresponding link-lengths

    @njit
    def _find_edge_candidate():
        # repeat until one linking attempt is successful:
        # draw a random node that receives another link:
        # ziehe einen Knotne zufällig; Dieser Knoten iwr dine neue Kante bekommen
        i = np.random.randint(0, N)
        Di = 1.0 * D[i, :]  # Das ist der Abstand aller Knoten zu diesem Knoten
        Di[i] = np.inf
        dmin = Di.min()  # finde den kleinsten Abstand zwischen dem gewählten un dinem anderen Knoten
        pmax = 1 / (1 + dmin / r0) ** gamma  # das ist dann die maximale Wahrscheinlichkeit einen Knoten zu ziehen
        # durch die Normierung pmax steigt die Wahrscheinlichkeit einen Knoten zu finden und die Rechenleistung wird verringert
        while True:
            # draw another random node:
            j = np.random.randint(0, N)
            if i == j:
                continue
            # compute linking probability:
            l = D[i, j]
            p = 1 / (1 + l / r0) ** gamma / pmax  # Die Wahrscheinlichkeit, dass sich 2 Knoten miteinander Verbinden
            # maybe link and leave:
            if np.random.rand() < p:
                return i, j, l
            # otherwise repeat

    def add_one_edge():
        # repeat until new edge is found:
        while True:
            i, j, l = _find_edge_candidate()
            # if new, add and leave:
            if A[i, j] == 0:
                A[i, j] = A[j, i] = 1  # das ist di adjacey Matrix, und wird symmstrisch verbunden
                L[i, j] = L[j, i] = l  # Das ist die Abstands Matrix und zeichnet den Abstand zwischen den Knoten auf
                return i, j, l
                # else repeat

    # add the edges:
    for r in range(M):
        add_one_edge()

    if make_connected:
        maxD = D.max()
        # find all connected components:
        n_components, node2component = connected_components(csgraph=A, directed=False)
        indices, sizes = np.unique(node2component, return_counts=True)
        # find giant component:
        giant_index = indices[np.argmax(sizes)]
        giant_nodes = np.where(node2component == giant_index)[0]
        # for each component other than giant component,
        # add random link to giant component:
        for index in indices:
            if index != giant_index:
                i = np.random.choice(np.where(node2component == index)[0])
                # find closest node in giant component:
                Di = D[i, :]
                Di[giant_nodes] -= 2 * maxD  # makes sure we ignore nodes outside giant component
                j = np.argmin(Di)
                A[i, j] = A[j, i] = 1
                L[i, j] = L[j, i] = D[i, j]
    del D

    return A, L


def generate_potentially_actives(A, node2country, country2P, corr):
    """For each country, generate a set of country2P many nodes of the network
    given by A, using an SI model in which the ratio between contagion and
    exploration is corr.

    @arg A: adjacency matrix, shape N by N
    @arg node2country: array of length N listing the country codes of all nodes
    @arg country2P: dictionary of number of potentially actives by country to choose
    @arg corr: (0 <= corr <= 1) parameter governing whether the picked nodes
               should be completely uncorrelated (corr=0) or form a connected
               set (corr=1). Default: 0

    @return is_pa: boolean array marking the potentially active nodes
    """
    N = A.shape[0]
    is_pa = np.zeros(N, dtype=type(True))

    non_pas = list(range(0, N))
    degrees = np.array(A.sum(axis=1)).flatten()
    n_pa_nbs = np.zeros(N, dtype="int")

    target_N_pa = np.sum(list(country2P.values()))  # total no. of wanted pas
    N_pa = 0  # total no. generated pas
    country2n_pa = {c: 0 for c in country2P.keys()}  # no. generated pas by country
    sum_shares = 0  # sum of n_pa_nbs/degree over all non_pas

    def make_pa(i, sum_shares):
        is_pa[i] = True
        non_pas.remove(i)
        # update sum_shares:
        sum_shares -= n_pa_nbs[i] / degrees[i]
        for j in A[i, :].nonzero()[1]:
            if not is_pa[j]:
                n_pa_nbs[j] += 1
                sum_shares += 1 / degrees[j]
        return sum_shares

    # pick an initial node:
    i = np.random.randint(0, N)
    N_pa += 1
    country2n_pa[node2country[i]] += 1
    sum_shares = make_pa(i, sum_shares)

    # simulate SI process until P many are potentially active:
    while N_pa < target_N_pa:
        # print(N_pa, target_N_pa)
        # probability that a randomly drawn non_pa will explore:
        w_explore = 1 - corr
        # probability that a randomly drawn non_pa will get infected:
        w_infect = corr * sum_shares / len(non_pas)
        # probability that next new pa is due to exploration:
        p_next_due_to_exploration = w_explore / (w_infect + w_explore)
        if np.random.rand() < p_next_due_to_exploration:
            # next new pa is due to exploration
            # all non-pas have the same probability to be this i:
            i = np.random.choice(non_pas)
        else:
            # next new pa is due to infection
            # each non-pa has a probability to be this i that is proportional to his share of pa nbs:
            i = np.random.choice(non_pas, p=(n_pa_nbs[non_pas] / degrees[non_pas]) / sum_shares)
        c = node2country[i]
        if country2n_pa[c] < country2P[c]:
            # this country is not yet "satisfied", so add i as new pa:
            N_pa += 1
            country2n_pa[c] += 1
            sum_shares = make_pa(i, sum_shares)
    return is_pa


def generate_adjacency_matrix_and_potentially_actives(N, lats, lons, land, country_shares_array,
                                                      potentially_active_connection_corr):
    # N = number of nodes
    mean_degree = 7

    # calculate distance matrix:
    D = get_D(lats=lats, lons=lons)

    node2country_list = []
    node2country_listshares = []
    for code in range(len(land)):
        for i in range(len(country_shares_array[:, 3])):
            if land[code] == country_shares_array[:, 3][i]:
                node2country_list.append(country_shares_array[:, 0][i])
                node2country_listshares.append((country_shares_array[:, 0][i], country_shares_array[:, 4][i]))
                break
            if i == len(country_shares_array[:, 3]) - 1 and land[code] != country_shares_array[:, 3][i]:
                node2country_list.append("rest")
                node2country_listshares.append(("rest", np.mean(country_shares_array[:, 4])))

    node2country = np.array(node2country_list)
    types_counts = Counter(node2country_list)
    occuring_countries = list(set(node2country_listshares))

    country2P = {}
    for i in range(len(occuring_countries)):
        country2P[occuring_countries[i][0]] = occuring_countries[i][1] * types_counts[occuring_countries[i][0]]

    corr = potentially_active_connection_corr

    A, L = generate_links(D=D, M=int(N * mean_degree / 2))
    is_pa = generate_potentially_actives(A=A, node2country=node2country, country2P=country2P, corr=corr)

    return A, L, D, is_pa

@njit
def fill_arrays_with_data(N, timesteps, statistical_analysis_array, is_active, is_affected,
                          certainly_actives, certainly_actives_array, certainly_inactives,
                          certainly_inactives_array):
    for time in range(timesteps):
        for node in range(N):
            statistical_analysis_array[time][node][0] = is_active[time][node]
            statistical_analysis_array[time][node][1] = is_affected[time][node]

    for node in range(N):
        for active in certainly_actives:
            if node == active:
                certainly_actives_array[node] = 1
        for inactive in certainly_inactives:
            if node == inactive:
                certainly_inactives_array[node] = 1

    return statistical_analysis_array, certainly_actives_array, certainly_inactives_array
