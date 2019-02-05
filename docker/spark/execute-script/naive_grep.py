import os
from datetime import datetime
import re
from optparse import OptionParser

from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import udf
from pyspark.sql.session import SparkSession
from pyspark.sql.types import BooleanType

REGEX = "^.*%s.*$"


class ProgramOptions:
    def __init__(self, server: str, port: int, in_file: str, regex: str, value: str, out: str):
        self.__server = server
        self.__port = port
        self.__in_file = in_file
        self.__regex = regex
        self.__value = value
        self.__out = out

    @property
    def server(self) -> str:
        return self.__server

    @property
    def port(self) -> int:
        return self.__port

    @property
    def in_file(self) -> str:
        return self.__in_file

    @property
    def regex(self) -> str:
        return self.__regex

    @property
    def value(self) -> str:
        return self.__value

    @property
    def out(self) -> str:
        return self.__out


def main():
    ops = parse_args()
    filtered_df = filter_rows(ops)
    write_result(ops, filtered_df)


def parse_args() -> ProgramOptions:
    op_parser = OptionParser()
    op_parser.add_option("-s", "--server", dest="server", help="Hadoop host name.")
    op_parser.add_option("-p", "--port", dest="port", type="int", help="Hadoop host port.")
    op_parser.add_option("-f", "--file", dest="file", help="Processed file hdfs path.")
    op_parser.add_option("-r", "--regex", dest="regex", help="Regex which will be searched.", default=REGEX)
    op_parser.add_option("-v", "--value", dest="value", help="Regex value.")
    op_parser.add_option("-o", "--out", dest="out", help="Output file path.", default="out.txt")

    ops, args = op_parser.parse_args()

    return ProgramOptions(ops.server, ops.port, ops.file, ops.regex, ops.value, ops.out)


def filter_rows(ops: ProgramOptions):
    spark_session = SparkSession.builder.appName("naive-grep").getOrCreate()
    in_file = "hdfs://%s:%d/%s" % (ops.server, ops.port, ops.in_file)
    df = spark_session.read.text(in_file)
    regex = ops.regex % ops.value.lower()
    pattern = re.compile(regex)

    def is_row_match(line):
        return bool(pattern.match(line.lower()))

    filter_is_match = udf(is_row_match, BooleanType())
    filtered_df = df.filter(filter_is_match(df.value)).select("value")

    return filtered_df


def write_result(ops: ProgramOptions, filtered_df: DataFrame):
    if is_write_on_hadoop(ops):
        write_to_hdfs(ops, filtered_df)
    else:
        write_to_local_file(ops, filtered_df)


def is_write_on_hadoop(ops: ProgramOptions) -> bool:
    return ops.out.startswith("hdfs://")


def write_to_local_file(ops: ProgramOptions, filtered_df):
    out = append_cuurent_time_to_filename(ops.out)
    with open(out, "w+") as out_file:
        for row in filtered_df.toLocalIterator():
            out_file.write("%s\n" % row)


def write_to_hdfs(ops: ProgramOptions, filtered_df: DataFrame):
    path = ops.out[6:]
    path = append_cuurent_time_to_filename(path)
    filtered_df.write.text(path)


def append_cuurent_time_to_filename(file: str) -> str:
    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = ".".join([os.path.basename(file), current_time])
    dirname = os.path.dirname(file)

    return os.path.join(dirname, filename)

main()
