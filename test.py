from pyspark import SparkContext

sc = SparkContext('local','example')


x = sc.textFile("dataset.txt").map(lambda v: v.split(":")).map(lambda v: (v[0], [v[1]])).reduceByKey(lambda v1, v2: v1 + v2).filter(lambda (k,v): k != "verb").flatMap(lambda (k, v): v)

y = x.map(lambda x: (x[0], x)).aggregateByKey(list(), lambda k,v: k+[v], lambda v1, v2: v1+v2)

z = x.map(lambda x: (x[-1], x)).aggregateByKey(list(), lambda k,v: k+[v], lambda v1, v2: v1+v2)

result = y.cartesian(z).map(lambda ((k1,v1), (k2, v2)): ((k1+k2), list(set(v1) & set(v2)))).filter(lambda (k,v): len(v) > 1).collect()

print(result)

input()
