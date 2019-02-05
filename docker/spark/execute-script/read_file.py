import re

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import BooleanType

spark_session = SparkSession.builder.appName("grep-app").getOrCreate()
df = spark_session.read.text("hdfs://hadoop-yarn:9000/user/root/datasets/epa-http.txt")
pattern = re.compile("^.*GET.*$")


def is_match(line):
    return bool(pattern.match(line))


filter_is_match = udf(is_match, BooleanType())
df = df.filter(filter_is_match(df.value)).select("value")
df.show(20, False)
with open("out.txt", "w+") as output_file:
    for row in df.toLocalIterator():
        output_file.write("%s\n" % row)
