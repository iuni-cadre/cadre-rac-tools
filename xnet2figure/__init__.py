
import sys
import os
import math

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import igraph as ig
import numpy as np

try:
	from . import xnet as xn
except ImportError as error:
	import xnet as xn

minYear = 2000
minKCore = 1

_styleColors = [
	"#1f77b4",
	"#ff7f0e",
	"#2ca02c",
	"#d62728",
	"#9467bd",
	"#8c564b",
	"#e377c2",
	"#7f7f7f",
	"#bcbd22",
	"#17becf",
	"#aec7e8",
	"#ffbb78",
	"#98df8a",
	"#ff9896",
	"#c5b0d5",
	"#c49c94",
	"#f7b6d2",
	"#c7c7c7",
	"#dbdb8d",
	"#9edae5",
];


# Draw the network. If there is community property, use that property as color, otherwise, use degree.

def xnet_to_figure(argv):
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
	xnet_input_to_figure(input_files[0], output_file)

def sortByFrequency(arr):
	s = set(arr)
	keys = {n: (-arr.count(n), arr.index(n)) for n in s}
	return sorted(list(s), key=lambda n: keys[n])

def convertColorToRGBAString(r,g,b,a):
	return "rgba(%d,%d,%d,%f)"%(round(r*255),round(g*255),round(b*255),a)

from matplotlib import collections  as mc
def drawGraph(graph,ax):
	print(graph.vcount())
	print("Layouting...");
	#positions = np.array(graph.layout_drl());
	positions = np.array(graph.layout_lgl(maxiter=400,coolexp = 2.0));
	print("Plotting...");
	linesX = []
	linesY = []
	segments = []
	positionsX = positions[:,0]
	positionsY = positions[:,1]
	for edge in graph.es:
		source = edge.source
		target = edge.target
		fx = positionsX[source]
		fy = positionsY[source]
		tx = positionsX[target]
		ty = positionsY[target]
		linesX.append(fx)
		linesX.append(tx)
		linesX.append(None)
		linesY.append(fy)
		linesY.append(ty)
		linesY.append(None)
		segments.append([(fx, fy), (tx, ty)])
	# plt.plot(linesX,linesY,alpha=0.1);
	lc = mc.LineCollection(segments, colors=graph.es["color"], linewidths=1.5)
	ax.add_collection(lc)
	print("Finished Plotting...");
	ax.scatter(positionsX,positionsY,marker="o",c=graph.vs["color"],s=graph.vs["vertex_size"],zorder=10);
	ax.autoscale()
	ax.margins(0.01)
	
def xnet_input_to_figure(input_file, output_file,minYear=minYear,minKCore=minKCore):
	originalGraph = xn.xnet2igraph(input_file)
	graph = originalGraph.clusters(mode="WEAK").giant()
	verticesToDelete = np.where(np.logical_or(np.array(graph.vs["year"])<minYear,np.array(graph.vs["KCore"])<minKCore))[0]
	graph.delete_vertices(verticesToDelete)
	graph = graph.clusters(mode="WEAK").giant()
	
	indegree = graph.indegree()
	maxIndegree = max(indegree);
	graph.vs["vertex_size"] = [x/maxIndegree*10+4 for x in indegree]
	
	colormap = plt.get_cmap("plasma");

	if("Community" not in graph.vertex_attributes()):
		graph.vs["color"] = [convertColorToRGBAString(*colormap(math.log(value+1))) for value in indegree]
	else:
		communities = graph.vs["Community"];
		sortedCommunities = sortByFrequency(communities);
		communityToColor = {community:(_styleColors[index] if index<len(_styleColors) else "#aaaaaa") for index,community in enumerate(sortedCommunities)};
		graph.vs["color"] = [communityToColor[community] for community in communities];
	
	for edgeIndex in range(graph.ecount()):
		sourceIndex = graph.es[edgeIndex].source;
		graph.es[edgeIndex]['color'] = graph.vs["color"][sourceIndex]+"20"

	fig, ax = plt.subplots(figsize=(10,10))
	drawGraph(graph,ax)
	plt.axis("off")
	plt.savefig(output_file)
	plt.close()
	# ig.plot(graph,output_file, **visual_style)

def xnet_query_id_to_figure(queryID,minYear=minYear,minKCore=minKCore):
	os.makedirs("figures", exist_ok=True)
	xnet_input_to_figure(
		"networks/%s.xnet"%queryID,
		"figures/%s_vis.pdf"%queryID,
		minYear=minYear,
		minKCore=minKCore
	)

if __name__ == "__main__":
	argv = sys.argv
	xnet_to_figure(argv)

