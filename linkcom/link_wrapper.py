# This is a wrapper for the link_clustering program
# developed by Jim Bagrow and Yong-Yeol Ahn
# It is made to run with python 3.5 and can
# be used with networkx graphs. The wrapper does
# not print anything out to file unless specified
# Modified: 2016-10-16
# Nathaniel Rodriguez

from collections import defaultdict
import networkx as nx
import .link_clustering as lc

def convert_to_lc_format(graph, is_weighted, weight_key):

    adj = defaultdict(set)
    edges = set()
    ij2wij = {}
    for ni, nj in graph.edges_iter():
        if is_weighted:
            wij = graph[ni][nj][weight_key]
        else:
            wij = 1
            
        if ni != nj: # skip any self-loops...
            ni,nj = lc.swap(ni,nj)
            edges.add( (ni,nj) )
            ij2wij[ni,nj] = wij
            adj[ni].add(nj)
            adj[nj].add(ni)

    return dict(adj), edges, ij2wij

def cluster(nx_graph, threshold=None, is_weighted=False, weight_key='weight', 
    dendro_flag=False, to_file=False, basename="clustering", delimiter='\t'):

    """
    ARGUMENTS:
    nx_graph        a networkx graph of type(G) = Graph. No parallel edges or self-loops. Undirected.
    threshold       the threshold parameter for lc (defaults to None)
    weight_key      the attribute key used by the networkx graph for weights (usually defaults to weight)
    dendro_flag     if unweighted and no threshold was given, then a dendrogram can be returned (defaults to False)
    to_file         specifies whether to write output to file (defaults to false)
    basename        specifies name use for files if to_file is True
    delimiter       delimiter to use when writting to file

    OUTPUT:
    if no threshold: returns a tuple with: (dict) dictionary with keys=edges and values=community membership, 
                    (float) max similarity, (float) max partition density, (list) partition density list

    if dendro_flag: returns a tuple with: (dict) dictionary with keys=edges and values=community membership, 
                    (float) max similarity, (float) max partition density, (list) partition density list,
                    (dict) keys=edges and values=community membership for original, (list) dendrogram

    if threshold: returns a tuple with: (dict) dictionary with keys=edges and values=community membership, partition density at threshold
    """

    if type(nx_graph).__name__ != 'Graph':
        raise TypeError("Graph must be simple (no parallel edges or self-loops) and undirected. See networkx documentation for how to convert graph to simple Graph.")

    adj, edges, ij2wij = convert_to_lc_format(nx_graph, is_weighted, weight_key)
    
    if threshold is not None:
        if is_weighted:
            edge2cid,D_thr = lc.HLC( adj,edges ).single_linkage( threshold, w=ij2wij )
        else:
            edge2cid,D_thr = lc.HLC( adj,edges ).single_linkage( threshold )
        print("# D_thr = " , D_thr)
        if to_file:
            lc.write_edge2cid( edge2cid,"{:s}_thrS{:f}_thrD{:f}".format(basename,threshold,D_thr), delimiter=delimiter )

    else:
        if is_weighted:
            edge2cid,S_max,D_max,list_D = lc.HLC( adj,edges ).single_linkage( w=ij2wij )
        else:
            if dendro_flag:
                edge2cid,S_max,D_max,list_D, orig_cid2edge, linkage = lc.HLC( adj,edges ).single_linkage( 
                                                                                dendro_flag=dendro_flag )
                if to_file:
                    lc.write_dendro( "{:s}_dendro".format(basename), orig_cid2edge, linkage)
            else:
                edge2cid,S_max,D_max,list_D = lc.HLC( adj,edges ).single_linkage()

        print("# D_max = {:f}\n# S_max = {:f}".format(D_max,S_max))
        if to_file:
            f = open("{:s}_thr_D.txt".format(basename),'w')
            for s,D in list_D:
                print(s, D, end="\n", file=f)
            f.close()
            lc.write_edge2cid( edge2cid,"{:s}_maxS{:f}_maxD{:f}".format(basename,S_max,D_max), delimiter=delimiter )

    if threshold is not None:
        return edge2cid, D_thr
    else:
        if dendro_flag:
            return edge2cid, S_max, D_max, list_D, orig_cid2edge, linkage

        return edge2cid, S_max, D_max, list_D

if __name__ == '__main__':
    """
    """
    pass