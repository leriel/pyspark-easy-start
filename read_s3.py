import sys, os
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
from subprocess import check_output

spark_conf = SparkConf()

SPARK_DRIVER_HOST = check_output(["hostname", "-i"]).decode(encoding="utf-8").strip()
spark_conf.setAll(
    [
        (
            "spark.master",
            "spark://spark:7077",
        ),  # <--- this host must be resolvable by the driver in this case pyspark (whatever it is located, same server or remote) in our case the IP of server
        ("spark.app.name", "myApp"),
        ("spark.submit.deployMode", "client"),
        ("spark.ui.showConsoleProgress", "true"),
        ("spark.eventLog.enabled", "false"),
        ("spark.logConf", "false"),
        (
            "spark.driver.bindAddress",
            "0.0.0.0",
        ),  # <--- this host is the IP where pyspark will bind the service running the driver (normally 0.0.0.0)
        (
            "spark.driver.host",
            SPARK_DRIVER_HOST,
        ),  # <--- this host is the resolvable IP for the host that is running the driver and it must be reachable by the master and master must be able to reach it (in our case the IP of the container where we are running pyspark
    ]
)

s3_key = "S3_KEY"
s3_secret = "S3_SECRET"
s3_endpoint = "S3_ENDPOINT_WITHOUT_HTTPS"

spark_sess = SparkSession.builder.config(conf=spark_conf).getOrCreate()
sc = spark_sess.sparkContext
hadoop_conf = sc._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.access.key", s3_key)
hadoop_conf.set("fs.s3a.secret.key", s3_secret)
hadoop_conf.set("fs.s3a.endpoint", s3_endpoint)
hadoop_conf.set("fs.s3a.impl","org.apache.hadoop.fs.s3a.S3AFileSystem")
# use path style access for minio. Do not use for aws s3
# for s3, set to "false"
hadoop_conf.set("fs.s3a.path.style.access", "true")
df = spark_sess.read.csv("s3a://bucket-name/path/to/file.csv")
print(df)

spark_sess.stop()
quit()
