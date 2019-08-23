
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
	input_files = []
	output_files = []
	if ',' in input_file_string:
		input_file_string = "" + input_file_string + ""
		input_files = input_file_string.split(",")
	else:
		input_files.append(input_file_string)
	if ',' in output_files_string:
		output_files_string = "" + output_files_string + ""
		output_files = output_files_string.split(',')
	else:
		output_files.append(output_files_string)
	
	output_file = output_location + '/' + output_files[0]
	xnet_input_to_communities(input_files[0], output_file)

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
