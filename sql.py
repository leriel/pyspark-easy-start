import sys, os
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import Row
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

spark_sess = SparkSession.builder.config(conf=spark_conf).getOrCreate()
spark_reader = spark_sess.read

myDF = spark_sess.createDataFrame(
    [
        Row(col0=0, col1=1, col2=2),
        Row(col0=3, col1=1, col2=5),
        Row(col0=6, col1=2, col2=8),
    ]
)

myGDF = myDF.select("*").groupBy("col1")
myDF.createOrReplaceTempView("mydf_as_sqltable")
print(myDF.collect())
myGDF.sum().show()

spark_sess.stop()
quit()
