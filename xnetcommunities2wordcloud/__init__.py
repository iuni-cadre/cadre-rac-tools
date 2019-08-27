
import sys
import os
import math
import random

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import igraph as ig
from wordcloud import WordCloud
import numpy as np

try:
	from . import xnet as xn
except ImportError as error:
	import xnet as xn

maxInternalWords = 300
maxAllWords = 1000
maxCommunities = 4;
minYear= 2000
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

def lighten_color(color, amount=0.5):
	"""
	Lightens the given color by multiplying (1-luminosity) by the given amount.
	Input can be matplotlib color string, hex string, or RGB tuple.
	
	Examples:
	>> lighten_color('g', 0.3)
	>> lighten_color('#F034A3', 0.6)
	>> lighten_color((.3,.55,.1), 0.5)
	"""
	import matplotlib.colors as mc
	import colorsys
	try:
		c = mc.cnames[color]
	except:
		c = color
	c = colorsys.rgb_to_hls(*mc.to_rgb(c))
	return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


def generateColorFunction(originalColor):
	def lighten_color_func(word, font_size, position, orientation, random_state=None,**kwargs):
		c = lighten_color(originalColor,font_size/200*0.6+0.2+0.4*random.random())
		return (int(c[0]*255),int(c[1]*255),int(c[2]*255))
	return lighten_color_func



#Extract major component and obtain community structure using infomap

def xnet_to_communities_wordcloud(argv):
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
	xnet_input_to_communities_wordcloud(input_files[0], output_file)

def sortByFrequency(arr):
	s = set(arr)
	keys = {n: (-arr.count(n), arr.index(n)) for n in s}
	return sorted(list(s), key=lambda n: keys[n])
 
def xnet_input_to_communities_wordcloud(input_file, output_file,minYear=minYear,minKCore=minKCore):
	graph = xn.xnet2igraph(input_file)
	verticesToDelete = np.where(np.logical_or(np.array(graph.vs["year"])<minYear,np.array(graph.vs["KCore"])<minKCore))[0]
	graph.delete_vertices(verticesToDelete)
	graph = graph.clusters(mode="WEAK").giant()
	communities = graph.vs["Community"]
	sortedCommunities = sortByFrequency(communities)[0:maxCommunities]
	fig = plt.figure(figsize=(20,5*math.ceil(len(sortedCommunities)/2)))
	allAbstracts = "\n".join(graph.vs["paper_abstract"])
	allFrequencies = WordCloud(max_words=maxAllWords).process_text(allAbstracts)
	amask = np.zeros((500,1000),dtype='B')
	amask[:10,:] = 255
	amask[-10:,:] = 255
	amask[:,:10] = 255
	amask[:,-10:] = 255
	for index,community in enumerate(sortedCommunities):
		communityColor = (_styleColors[index] if index<len(_styleColors) else "#aaaaaa")
		abstracts = "\n".join([vertex["paper_abstract"] for vertex in graph.vs if vertex["Community"]==community])
		plt.subplot(math.ceil(len(sortedCommunities)/2),2,index+1)
		wc = WordCloud(background_color="white", max_words=maxInternalWords, width=1000,height=500,
			mask=amask,contour_width=10, contour_color=communityColor,random_state=3,color_func=generateColorFunction(communityColor))
		
		inCommunityFrequency = wc.process_text(abstracts)
		relativeFrequencies = {key:frequency/math.log(allFrequencies[key]+1) for key,frequency in inCommunityFrequency.items() if key in allFrequencies}
		wc.generate_from_frequencies(relativeFrequencies)
		
		plt.imshow(wc, interpolation='bilinear')
		plt.axis("off")
		
	plt.tight_layout()
	plt.savefig(output_file)
	plt.close(fig)

def xnet_query_id_to_communities_wordcloud(queryID,minYear=minYear,minKCore=minKCore):
	os.makedirs("figures", exist_ok=True)
	xnet_input_to_communities_wordcloud(
		"networks/%s.xnet"%queryID,
		"figures/%s_communities_wc.pdf"%queryID,
		minYear=minYear,
		minKCore=minKCore
	)

if __name__ == "__main__":
	argv = sys.argv
	xnet_to_communities_wordcloud(argv)


