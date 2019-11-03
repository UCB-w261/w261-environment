import pyspark
import numpy as np
import pandas as pd
from pyspark.sql import SQLContext
import itertools



def naive(df, ranks=[2,4]):
    def findRankStatistics(df, ranks):
        assert (all([rank > 0 for rank in ranks]))  ## require all ranks to be > 0

        numCols = len(df.schema)
        i = 0
        results = {}
        for i in range(numCols):
            col = df.rdd.map(lambda row: row[i])
            sortedCol = col.sortBy(lambda x: x).zipWithIndex()
            ranksOnly = sortedCol.filter(
                lambda (colValue, index): (index + 1) in ranks
            ).keys()
            rankedList = ranksOnly.collect()
            results[i + 1] = rankedList
        return results

    return findRankStatistics(df, ranks)

def group_by(df, ranks=[2,4]):
    def mapToKeyValuePairs(df):
        rowLength = len(df.schema)
        return df.rdd.flatMap(lambda row: [(i, row[i]) for i in range(0, rowLength)])

    def findRankStatistics(df, ranks):
        assert (all([rank > 0 for rank in ranks]))  ## require all ranks to be > 0

        pairRDD = mapToKeyValuePairs(df)
        groupColumns = pairRDD.groupByKey()

        def convertToArrayAndSort(iterable):
            sortedIter = list(iterable)
            sortedIter.sort()
            return [val for i, val in enumerate(sortedIter) if (i + 1) in ranks]

        ## mapValues doc: http://spark.apache.org/docs/latest/api/python/pyspark.html?highlight=mapvalues#pyspark.RDD.flatMapValues
        return groupColumns.mapValues(convertToArrayAndSort).collectAsMap()

    return findRankStatistics(df, ranks)

def secondary_sort(df, ranks=[2,4]):
    def ColumnIndexPartition(numPartitions):
        assert (numPartitions >= 0)
        """Partition by the first item in the key tuple"""

        def getPartition(x):
            return abs(x[0]) % numPartitions

        return getPartition

    def mapToKeyValuePairs(df):
        rowLength = len(df.schema)
        return df.rdd.flatMap(lambda row: [(i, row[i]) for i in range(0, rowLength)])

    def findRankStatistics(df, targetRanks, partitions):
        assert (all([rank > 0 for rank in targetRanks]))  ## require all ranks to be > 0

        pairRDD = mapToKeyValuePairs(df).map(lambda x: (x, 1))
        partitioner = ColumnIndexPartition(partitions)
        sorted = pairRDD.repartitionAndSortWithinPartitions(partitions, partitioner)

        def filterForTargetRanksFn(iterable):
            currentColumnIndex = [
                -1]  ## made these objects to be accessed in the filterFn without python scope problems
            runningTotal = [0]

            def filterFn(x):
                ((colIndex, value), _) = x
                if colIndex != currentColumnIndex[0]:
                    currentColumnIndex[0] = colIndex  ## reset to the new column index
                    runningTotal[0] = 1
                else:
                    runningTotal[0] += 1
                return runningTotal[0] in targetRanks

            return map(lambda x: x[0], filter(filterFn, iterable))

        filterForTargetIndex = sorted.mapPartitions(filterForTargetRanksFn, preservesPartitioning=True)
        results = filterForTargetIndex.collect()

        resultsMap = {}  ## just need to group them now
        for i, val in results:
            if i not in resultsMap:
                resultsMap[i] = []
            resultsMap[i].append(val)

        return resultsMap

    return findRankStatistics(df, ranks, 3)

def sort_on_cell_value(df, ranks=[2,4]):
    def getValueColumnPairs(dataFrame):
        return dataFrame.rdd.flatMap(lambda row: [(val, index) for index, val in enumerate(row)])

    def getColumnsFreqPerPartition(sortedValueColumnPairs, numOfColumns):
        zero = [0 for i in range(numOfColumns)]

        def aggregateColumnFrequencies(partitionIndex, valueColumnPairs):
            for val, index in valueColumnPairs:
                zero[index] += 1
            return [(partitionIndex, list(zero))]

        return sortedValueColumnPairs.mapPartitionsWithIndex(aggregateColumnFrequencies).collect()

    def getRanksLocationsWithinEachPart(targetRanks, partitionColumnsFreq, numOfColumns):
        runningTotal = [0 for i in range(numOfColumns)]

        def partitionColumnsFreqFn((partitionIndex, columnsFreq)):
            relevantIndexList = []
            for colIndex, colCount in enumerate(columnsFreq):
                runningTotalCol = runningTotal[colIndex]
                ranksHere = filter(lambda rank: runningTotalCol < rank and (runningTotalCol + colCount) >= rank,
                                   targetRanks)
                relevantIndexList += map(lambda rank: [colIndex, rank - runningTotalCol], ranksHere)
                runningTotal[colIndex] += colCount
            return [partitionIndex, filter(lambda x: x != [], relevantIndexList)]

        return map(partitionColumnsFreqFn, sorted(partitionColumnsFreq, key=lambda x: x[0]))

    def findTargetRanksIteratively(sortedValueColumnPairs, ranksLocations):
        def sortedValueColumnPairsFn(partitionIndex, valueColumnPairs):
            targetsInThisPart = ranksLocations[partitionIndex][1]
            if targetsInThisPart:
                columnsRelativeIndex = {}
                for k, g in itertools.groupby(sorted(targetsInThisPart), key=lambda x: x[0]):
                    columnsRelativeIndex[k] = [pair[1] for pair in g]
                columnsInThisPart = list(set(map(lambda x: x[0], targetsInThisPart)))
                runningTotals = {}
                for i in columnsInThisPart:
                    runningTotals[i] = 0

                def valueColumnPairsFn((value, colIndex)):
                    if colIndex not in runningTotals:
                        return False
                    total = runningTotals[colIndex] + 1
                    runningTotals[colIndex] = total
                    thisPairIsTheRankStatistic = total in columnsRelativeIndex[colIndex]
                    return thisPairIsTheRankStatistic

                return map(lambda (x, y): (y, x), filter(valueColumnPairsFn, valueColumnPairs))
            else:
                return iter([])
            return targetsInThisPart

        return sortedValueColumnPairs.mapPartitionsWithIndex(sortedValueColumnPairsFn)

    def findRankStatistics(dataFrame, targetRanks):
        valueColumnPairs = getValueColumnPairs(dataFrame)
        sortedValueColumnPairs = valueColumnPairs.sortByKey()
        sortedValueColumnPairs.persist(pyspark.StorageLevel.MEMORY_AND_DISK)
        numOfColumns = len(dataFrame.schema)
        partitionColumnsFreq = getColumnsFreqPerPartition(sortedValueColumnPairs, numOfColumns)
        ranksLocations = getRanksLocationsWithinEachPart(targetRanks, partitionColumnsFreq, numOfColumns)
        targetRanksValues = findTargetRanksIteratively(sortedValueColumnPairs, ranksLocations)

        results = targetRanksValues.collect()
        resultsMap = {}  ## just need to group them now
        for i, val in results:
            if i not in resultsMap:
                resultsMap[i] = []
            resultsMap[i].append(val)
        return resultsMap

    return findRankStatistics(df, ranks)

def reduce_to_distinct_by_partition(df, ranks=[2,4]):
    def getAggregatedValueColumnPairs(dataFrame):
        def aggregatedValueColumnFn(rows):
            valueColumnMap = {}
            for row in rows:
                row = list(row)
                for val, columnIndex in zip(row, range(len(row))):
                    key = (val, columnIndex)
                    if key in valueColumnMap:
                        valueColumnMap[key] = valueColumnMap[key] + 1
                    else:
                        valueColumnMap[key] = 1
            return valueColumnMap.items()

        aggregatedValueColumnRDD = dataFrame.rdd.mapPartitions(aggregatedValueColumnFn)
        return aggregatedValueColumnRDD

    def getColumnsFreqPerPartition(sortedAggregatedValueColumnPairs, numOfColumns):
        def aggregateColumnFrequencies(partitionIndex, valueColumnPairs):
            zero = [0 for i in range(numOfColumns)]
            for v in valueColumnPairs:
                ((value, colIndex), count) = v
                zero[colIndex] = zero[colIndex] + count
            return [(partitionIndex, zero)]
        return sortedAggregatedValueColumnPairs.mapPartitionsWithIndex(aggregateColumnFrequencies).collect()

    def getRanksLocationsWithinEachPart(targetRanks, partitionColumnsFreq, numOfColumns):
        runningTotal = [0 for i in range(numOfColumns)]
        partitionColumnsFreq = sorted(partitionColumnsFreq, key=lambda tup: tup[0])

        list_of_relevantIndex = []
        for partitionIndex, columnsFreq in partitionColumnsFreq:
            relevantIndexList = {}
            for colCount, colIndex in zip(columnsFreq, range(len(columnsFreq))):
                runningTotalCol = runningTotal[colIndex]
                ranksHere = filter(lambda rank: runningTotalCol < rank and runningTotalCol + colCount >= rank,
                                   targetRanks)
                for rank in ranksHere:
                    if colIndex in relevantIndexList:
                        relevantIndexList[colIndex] = relevantIndexList[colIndex] + rank - runningTotalCol
                    else:
                        relevantIndexList[colIndex] = rank - runningTotalCol
                runningTotal[colIndex] += colCount
            list_of_relevantIndex.append((partitionIndex, relevantIndexList.items()))

        return list_of_relevantIndex

    def asIteratorToIteratorTransformation(valueColumnPairsIter, targetsInThisPart):
        ## {1: [1], 2: [1]}
        columnsRelativeIndex = dict(
            [(k, [n[1] for n in g]) for k, g in itertools.groupby(targetsInThisPart, key=lambda x: x[0])])
        columnsInThisPart = list(set(i[0] for i in targetsInThisPart))
        runningTotals = {}
        for col in columnsInThisPart:
            runningTotals[col] = 0
        pairsWithRanksInThisPart = filter(lambda ((value, colIndex), count): colIndex in columnsInThisPart,
                                          valueColumnPairsIter)

        returnList = []
        for ((value, colIndex), count) in pairsWithRanksInThisPart:
            total = runningTotals[colIndex]
            ranksPresent = filter(lambda index: (index <= count + total) and (index > total),
                                  columnsRelativeIndex[colIndex])
            nextElems = [(colIndex, value) for r in ranksPresent]
            runningTotals[colIndex] = total + count
            returnList += nextElems
        return returnList

    def findTargetRanksIteratively(sortedAggregatedValueColumnPairs, ranksLocations):
        def sortedAggregatedValueColumnPairsFn(partitionIndex, aggregatedValueColumnPairs):
            targetsInThisPart = ranksLocations[partitionIndex][1]
            if targetsInThisPart and len(targetsInThisPart) > 0:
                return asIteratorToIteratorTransformation(aggregatedValueColumnPairs, targetsInThisPart)
            else:
                return []

        return sortedAggregatedValueColumnPairs.mapPartitionsWithIndex(sortedAggregatedValueColumnPairsFn)

    def findRankStatistics(dataFrame, targetRanks):
        aggregatedValueColumnPairs = getAggregatedValueColumnPairs(dataFrame)
        sortedAggregatedValueColumnPairs = aggregatedValueColumnPairs.sortByKey()
        sortedAggregatedValueColumnPairs.persist(pyspark.StorageLevel.MEMORY_AND_DISK)
        numOfColumns = len(dataFrame.schema)
        partitionColumnsFreq = getColumnsFreqPerPartition(sortedAggregatedValueColumnPairs, numOfColumns)
        ranksLocations = getRanksLocationsWithinEachPart(targetRanks, partitionColumnsFreq, numOfColumns)
        targetRanksValues = findTargetRanksIteratively(sortedAggregatedValueColumnPairs, ranksLocations)

        results = targetRanksValues.collect()
        resultsMap = {}  ## just need to group them now
        for i, val in results:
            if i not in resultsMap:
                resultsMap[i] = []
            resultsMap[i].append(val)
        return resultsMap

    return findRankStatistics(df, ranks)


sc = pyspark.SparkContext()
sqlCtx = SQLContext(sc)

names = ["Mama Panda", "Papa Panda", "Baby Panda", "Baby Panda's toy Panda"]
happiness = [15.0, 2.0, 10.0, 3.0]
niceness = [0.25, 1000, 2.0, 8.5]
softness = [2467.0, 35.4, 50.0, 0.2]
sweetness = [0.0, 0.0, 0.0, 98.0]

df = pd.DataFrame({"happiness": happiness, "niceness": niceness, "softness": softness, "sweetness": sweetness})
df.insert(0, 'panda_name', names)

print df.head()

df = sqlCtx.createDataFrame(df)

print naive(df)
print group_by(df)
print secondary_sort(df)
print sort_on_cell_value(df)
print reduce_to_distinct_by_partition(df)
