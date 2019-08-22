import sys
import os

import igraph as ig
import pandas as pd
import numpy as np

import xnet as xn

MAGColumnTypes = {
    "journal_id": object,
    "issue": object,
    "first_name": object,
    "last_name": object,
    "volume": object,
    "conference_instance_id": object,
    "conference_series_id": object,
    "doc_type": object,
    "doi": object,
    "original_venue": object,
    "publisher": object,
    "authors_last_known_affiliation_id": object,
    "field_of_study_id": object,
    "paper_publisher": object,
    "journal_display_name": object,
    "journal_issn": object,
    "paper_first_page": object,
    "paper_reference_id": object,
    "paper_abstract": object,
    "book_title": object,
    "conference_display_name": object,
    "journal_publisher": object,
    "paper_last_page": object,
}


def mag_query_to_xnet(argv):
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

    for input_file in input_files:
        if 'edges' in input_file:
            edges_file = input_file
        else:
            nodes_file = input_file

    output_file = output_location + '/' + output_files[0]
    mag_query_input_to_xnet(nodes_file, edges_file, output_file)


def mag_query_input_to_xnet(nodes_file, edges_file, output_file):
    edgesData = pd.read_csv(edges_file)
    nodesData = pd.read_csv(nodes_file, dtype=MAGColumnTypes)

    # Replacing NaN for empty string
    for key in MAGColumnTypes:
        if (key in nodesData):
            nodesData[key].fillna("", inplace=True)

    # Generating continous indices for papers
    index2ID = nodesData["paper_id"].tolist()
    ID2Index = {id: index for index, id in enumerate(index2ID)}

    # Hack to account for 2 degree capitalized "FROM"
    fromKey = "From"
    if (fromKey not in edgesData):
        fromKey = "FROM"

    # Converting edges from IDs to new indices
    # Invert edges so it means a citation between from to to
    edgesZip = zip(edgesData[fromKey].tolist(), edgesData["To"].tolist())
    edgesList = [(ID2Index[toID], ID2Index[fromID]) for fromID, toID in edgesZip if
                 fromID in ID2Index and toID in ID2Index]

    vertexAttributes = {key: nodesData[key].tolist() for key in nodesData}

    for key in nodesData:
        nodesData[key].tolist()

    graph = ig.Graph(
        n=len(index2ID),
        edges=edgesList,
        directed=True,
        vertex_attrs=vertexAttributes
    )

    # verticesToDelete = np.where(np.logical_or(np.array(graph.indegree())==0,np.array(graph.degree())==0))[0]
    # graph.delete_vertices(verticesToDelete)

    graph.vs["KCore"] = graph.shell_index(mode="IN")
    graph.vs["year"] = [int(s[0:4]) for s in graph.vs["date"]]
    xn.igraph2xnet(graph, output_file)


def mag_query_id_to_xnet(queryID):
    os.makedirs("../networks", exist_ok=True)
    mag_query_input_to_xnet(
        "query-results/%s.csv" % queryID,
        "query-results/%s_edges.csv" % queryID,
        "networks/" + queryID + ".xnet"
    )


if __name__ == "__main__":
    argv = sys.argv
    mag_query_to_xnet(argv)
