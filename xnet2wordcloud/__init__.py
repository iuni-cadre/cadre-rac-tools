
import sys
import os

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import igraph as ig
from wordcloud import WordCloud

try:
	from . import xnet as xn
except ImportError as error:
	import xnet as xn


#Extract major component and obtain community structure using infomap

def xnet_to_wordcloud(argv):
	input_file_string = argv[1]
	input_dir = argv[2]
	output_dir = argv[3]
	input_files = []
	if ',' in input_file_string:
		input_file_string = "" + input_file_string + ""
		input_file_names = input_file_string.split(",")
		for file_name in input_file_names:
			input_files.append(input_dir + "/" + file_name)
	else:
		input_files.append(input_dir + "/" + input_file_string)

	output_file = output_dir + '/output_wc.xnet'
	xnet_input_to_wordcloud(input_files[0], output_file)

def xnet_input_to_wordcloud(input_file, output_file):
	graph = xn.xnet2igraph(input_file)
	wc = WordCloud(background_color="white", max_words=2000, scale=10,
		contour_width=3, contour_color='white')
	wc.generate("\n".join(graph.vs["paper_abstract"]))
	wc.to_file(output_file)

def xnet_query_id_to_wordcloud(queryID):
	os.makedirs("figures", exist_ok=True)
	xnet_input_to_wordcloud(
		"networks/%s.xnet"%queryID,
		"figures/%s_wordcloud.pdf"%queryID
	)

if __name__ == "__main__":
	argv = sys.argv
	xnet_to_wordcloud(argv)
