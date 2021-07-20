# Pyspark easy start

This repo shows how to easily get started with local spark cluster (one master, one worker) and run pyspark jobs on it, provided you have docker.

## How to use
```
docker-compose up -d
docker-compose exec work-env sql.py
```

Sample output:
```
Creating network "mg-spark_default" with the default driver
Creating mg-spark_spark_1          ... done
Creating mg-spark_spark-worker-1_1 ... done
Creating mg-spark_work-env_1       ... done
21/03/05 15:56:21 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
21/03/05 15:56:25 WARN SparkContext: Please ensure that the number of slots available on your executors is limited by the number of cores to task cpus and not another custom resource. If cores is not the limiting resource then dynamic allocation will not work properly!
[Row(col0=0, col1=1, col2=2), Row(col0=3, col1=1, col2=5), Row(col0=6, col1=2, col2=8)]
+----+---------+---------+---------+
|col1|sum(col0)|sum(col1)|sum(col2)|
+----+---------+---------+---------+
|   1|        3|        2|        7|
|   2|        6|        2|        8|
+----+---------+---------+---------+
```

There are also `run_sql.sh`, `run_file.sh` and `run_s3.sh` scripts working for mac and linux.

Feel free to edit either of the .py files provided or create new ones. However, make sure any new files are inside same directory.

## Requirements:
* [docker](https://docs.docker.com/get-docker/)
* [docker-compose](https://docs.docker.com/compose/install/)

## No need to have:
* python. It is provided in the `bitnami/spark:3-debian-10` image
* pyspark. It is already installed inside `bitnami/spark:3-debian-10` image

## Note about local file access

`read_file.py` reads file from local filesystem. However, it's the worker that actually reads the file. Because of that there is `volumes` section defined for each docker service:
```
    volumes:
      - .:/app
```
so that the "local" file path resolves same way for every node.

## Note about s3 / google cloud storage

Please update `run_s3.py` with s3 credentials (and endpoint if running own s3 service) file to run the s3 example. Credentials are provided inside python code which is not optimal - please do not do that for files going into any code repository.

To properly provide credentials and other info like s3 endpoint, you will probably have to use workers to propagate them (perhaps env vars?). I haven't researched this aspect yet.

## Credits:
* Bitnami for their easy to use [image](https://hub.docker.com/r/bitnami/spark/)
* @dani8art for excellent [explaination](https://github.com/bitnami/bitnami-docker-spark/issues/18#issuecomment-700628676) how to connect to cluster from pyspark
