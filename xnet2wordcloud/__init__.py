
import sys

import igraph as ig

from wordcloud import WordCloud, STOPWORDS


try:
	from . import xnet as xn
except ImportError as error:
	import xnet as xn


#Extract major component and obtain community structure using infomap

def xnet_to_wordcloud(argv):
	input_file_string = argv[3]
	output_files_string = argv[4]
	output_location = argv[5]

	output_file = output_location + '/' + output_files_string
	xnet_input_to_wordcloud(input_file_string, output_file)

def xnet_input_to_wordcloud(input_file, output_file):
	graph = xn.xnet2igraph(input_file)
	wordcloud = WordCloud()
	wc = WordCloud(background_color="white", max_words=2000, scale=10,
		contour_width=3, contour_color='white')
	wordcloud.generate("\n".join(graph.vs["paper_abstract"]))
	wordcloud.to_file(output_file)

def xnet_query_id_to_wordcloud(queryID):
	xnet_input_to_wordcloud(
		"networks/%s.xnet"%queryID,
		"networks/%s_wordcloud.pdf"%queryID
	)

if __name__ == "__main__":
	argv = sys.argv
	xnet_to_wordcloud(argv)
