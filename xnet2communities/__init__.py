
import sys

import igraph as ig

try:
	from . import xnet as xn
except ImportError as error:
	import xnet as xn


#Extract major component and obtain community structure using infomap
def xnet_to_communities(argv):
	input_file_string = argv[3]
	output_files_string = argv[4]
	output_location = argv[5]

	output_file = output_location + '/' + output_files_string
	xnet_input_to_communities(input_file_string, output_file)

def xnet_input_to_communities(input_file, output_file):
	graph = xn.xnet2igraph(input_file)
	giantComponent = graph.clusters(mode="WEAK").giant()
	giantComponent.vs["Community"] = [str(c) for c in giantComponent.community_infomap().membership]
	xn.igraph2xnet(giantComponent,output_file)

def xnet_query_id_to_communities(queryID):
	xnet_input_to_communities(
		"networks/%s.xnet"%queryID,
		"networks/%s_communities.xnet"%queryID
	)

if __name__ == "__main__":
	argv = sys.argv
	xnet_to_communities(argv)
