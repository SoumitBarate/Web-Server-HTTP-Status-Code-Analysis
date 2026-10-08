# Web Server HTTP Status Code Analysis

## 1. Problem Statement

A company stores web server access logs in HDFS. The goal is to analyze the logs and count the number of requests for each HTTP status code.

Examples:

* `200` → Successful request
* `404` → Page not found
* `500` → Server error

## 2. Objective

The Hadoop MapReduce program:

1. Reads web server logs from HDFS.
2. Extracts the HTTP status code.
3. Generates `(status_code, 1)` from the Mapper.
4. Uses a Combiner for local aggregation.
5. Uses a Partitioner to distribute keys among Reducers.
6. Groups the same status codes during Shuffle and Sort.
7. Calculates the final count using the Reducer.
8. Stores the output in HDFS.

## 3. Technology Used

| Component            | Technology                      |
| -------------------- | ------------------------------- |
| Operating System     | Ubuntu / WSL                    |
| Programming Language | Python                          |
| Processing           | Hadoop MapReduce                |
| Storage              | HDFS                            |
| Mapper               | Python                          |
| Combiner             | Python                          |
| Partitioner          | Hadoop KeyFieldBasedPartitioner |
| Reducer              | Python                          |
| Execution            | Hadoop Streaming                |
| Input                | Text file                       |
| Output               | HDFS                            |

## 4. Project Files

```text
Web Server HTTP Status Code Analysis/
│
├── mapper.py
├── combiner.py
├── reducer.py
├── web_logs.txt
└── README.md
```

## 5. Input

Example input:

```text
192.168.1.10 GET /home 200
192.168.1.11 GET /login 200
192.168.1.12 GET /product 404
192.168.1.13 GET /home 200
192.168.1.14 GET /checkout 500
192.168.1.15 GET /product 404
192.168.1.16 GET /home 200
192.168.1.17 GET /server 500
```

## 6. Map Stage

The Mapper extracts the HTTP status code.

Example:

```text
192.168.1.10 GET /home 200
```

Mapper output:

```text
200    1
```

Another example:

```text
192.168.1.12 GET /product 404
```

Mapper output:

```text
404    1
```

## 7. Combiner Stage

The Combiner performs local aggregation before data is transferred to the Reducer.

Example:

```text
200    1
200    1
200    1
404    1
```

Combiner output:

```text
200    3
404    1
```

The Combiner reduces the amount of intermediate data transferred over the network.

> Combiner is a local mini-reducer. Hadoop does not guarantee that a Combiner will always execute.

## 8. Partitioner Stage

The Partitioner decides which Reducer receives each key.

In this project, Hadoop's `KeyFieldBasedPartitioner` is used.

Example:

```text
200 → Reducer 0
404 → Reducer 1
500 → Reducer 1
```

The important rule is that all values belonging to the same key must go to the same Reducer.

## 9. Shuffle and Sort

Hadoop groups values belonging to the same status code.

Conceptually:

```text
200 → [1,1,1,1]
404 → [1,1]
500 → [1,1]
```

## 10. Reduce Stage

The Reducer adds the values for each status code.

```text
200 → 4
404 → 2
500 → 2
```

## 11. Execution

### 1. Upload input file to HDFS

```bash
hdfs dfs -mkdir -p /usecase1/input
hdfs dfs -put web_logs.txt /usecase1/input
```

### 2. Remove previous output if it exists

```bash
hdfs dfs -rm -r -f /usecase1/output
```

### 3. Run Hadoop Streaming

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
-input /usecase1/input \
-output /usecase1/output \
-mapper mapper.py \
-combiner combiner.py \
-reducer reducer.py \
-files mapper.py,combiner.py,reducer.py \
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
-D stream.num.map.output.key.fields=1 \
-D mapreduce.job.reduces=2
```

### 4. View the output

```bash
hdfs dfs -cat /usecase1/output/part-*
```

## 12. Expected Output

```text
200    4
404    2
500    2
```

Meaning:

* HTTP `200` → 4 requests
* HTTP `404` → 2 requests
* HTTP `500` → 2 requests

## 13. MapReduce Flow

```text
Web Server Logs
       |
       v
      HDFS
       |
       v
    Mapper
       |
       v
(status_code, 1)
       |
       v
    Combiner
       |
       v
  Partitioner
       |
       v
 Shuffle & Sort
       |
       v
    Reducer
       |
       v
      HDFS
       |
       v
 Final Output
```

## 14. Learning Outcome

This use case demonstrates:

* Hadoop Streaming
* MapReduce
* Mapper
* Combiner
* Partitioner
* Shuffle and Sort
* Reducer
* HDFS
* HTTP status code analysis
