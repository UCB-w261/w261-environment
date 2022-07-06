# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
This is an example implementation of PageRank. For more conventional use,
Please refer to PageRank implementation provided by graphx
Example Usage:
bin/spark-submit examples/src/main/python/pagerank.py data/mllib/pagerank_data.txt 10
"""
from __future__ import print_function

import re
import sys
import ast
from operator import add

from pyspark.sql import SparkSession

def quiet_logs( sc ):
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org"). setLevel( logger.Level.ERROR )
    logger.LogManager.getLogger("akka").setLevel( logger.Level.ERROR )


def computeContribs(row):
    """
    Calculates URL contributions to the rank of other URLs.
    input: (1, ([], 1.0))
    """
    node, (edges, rank) = row
    num_edges = len(edges)
    
    for edge in edges:
        yield (edge, rank/num_edges )
        
    yield (node,0)    


def parseNeighbors(line):
        """
        Helper function to identify potential danglers and
        write edges as a csv string for efficient aggregation.
        input: 4	{'1': 1, '2': 2}
        output: 4 [1,2,2]
        """
        node, edges = line.strip().split('\t')
        edge_string = []       
        for edge, count in ast.literal_eval(edges).items():
            # emit potential danglers w/ empty string
            yield (int(edge), [])
            # add this edge to our string of edges
            for cnt in range(int(count)):
                edge_string.append(int(edge))
        # finally yield this node w/ its string formatted edge list
        yield (int(node), edge_string)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: pagerank <file> <iterations>", file=sys.stderr)
        sys.exit(-1)

    print("WARN: This is a naive implementation of PageRank and is given as an example!\n" +
          "Please refer to PageRank implementation provided by graphx",
          file=sys.stderr)

    # Initialize the spark context.
    spark = SparkSession\
        .builder\
        .appName("PythonPageRank")\
        .getOrCreate()

    quiet_logs( spark.sparkContext )
    
    # Loads in input file. It should be in format of:
    # 4	{'1': 1, '2': 2}
    
    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
    
    # Loads all URLs from input file and initialize their neighbors.
    links = lines.flatMap(lambda urls: parseNeighbors(urls)).reduceByKey(lambda a, b: a + b).cache()
#     N=links.count()
    
    # Loads all URLs with other URL(s) link to from input file and initialize ranks of them to one.
    ranks = links.map(lambda url_neighbors: (url_neighbors[0], 1.0))
    
    # Calculates and updates URL ranks continuously using PageRank algorithm.
    for iteration in range(int(sys.argv[2])):
        # Calculates URL contributions to the rank of other URLs.
        contribs = links.join(ranks).flatMap(
            lambda url_urls_rank: computeContribs(url_urls_rank))

        # Re-calculates URL ranks based on neighbor contributions.
        ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * 0.85 + 0.15)
    
    # Collects all URL ranks and dump them to console.
    for (link, rank) in sorted(ranks.collect(),key=lambda x: -x[1]):
        print("%s has rank: %s." % (link, rank))

    
    spark.stop()