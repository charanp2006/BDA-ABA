# Environment Report

Detected on 2026-10-30 before any project-specific assumptions were made.

## Host

| Item | Value |
|---|---|
| Operating system | Windows 11 (build 10.0.26300), accessed through Git Bash / MSYS2 (MINGW64) |
| Working directory | `C:\Charan\ABA\BDA-ABA` |
| Shell used | GNU Bash 3.6.6 (MINGW64) |
| Disk free on C: | ~196 GB at start |
| Git | 2.53.0.windows.2 |

## Tool detection (actual output)

| Tool | Command | Result |
|---|---|---|
| Java | `java -version` | Java 26 (build 26+35-2893), 64-bit |
| Hadoop | `hadoop version` | **not found** (`command not found`) |
| HDFS CLI | `hdfs dfs -ls /` | **not found** (`command not found`) |
| Hive CLI | `hive --version` | **not found** (`command not found`) |
| Beeline | `beeline --version` | **not found** (`command not found`) |
| Python | `python --version` | Python 3.14.3 |
| Docker Engine | `docker version` | Docker 29.8.0 (server reachable after starting Docker Desktop) |
| Docker Compose | `docker compose version` | v5.5.1 |

Python packages already installed: `pandas 3.0.2`, `numpy 2.4.4`,
`matplotlib 3.10.9`, `pytest 9.0.3`.

## Runtime decision

No native Hadoop, HDFS, Hive or Beeline installation exists on this Windows
host. The installed Java 26 is also far newer than the Java versions supported
by Hadoop 2.x/3.x, so a native installation would require a separate JDK.

To keep **HDFS + Apache Hive/HiveQL central and genuinely executed**, the
project runs the real services in Linux containers through Docker Desktop:

| Component | Image | Version |
|---|---|---|
| HDFS NameNode | `bde2020/hadoop-namenode` | Hadoop 2.7.4, Java 8 |
| HDFS DataNode | `bde2020/hadoop-datanode` | Hadoop 2.7.4, Java 8 |
| Hive Metastore / HiveServer2 | `bde2020/hive` | Apache Hive 2.3.2 |
| Metastore database | `bde2020/hive-metastore-postgresql` | PostgreSQL-backed Hive 2.3.0 schema |

Services exposed on the host:

- HDFS NameNode RPC: `hdfs://localhost:8020` (in-network: `hdfs://namenode:8020`)
- HDFS NameNode web UI: <http://localhost:50070>
- HiveServer2 JDBC: `jdbc:hive2://localhost:10000`
- Hive Metastore Thrift: `localhost:9083`

A custom `docker/hive-site.xml` is mounted into the Hive containers so Hive
uses the PostgreSQL metastore and HDFS rather than the default embedded Derby
database. `docker/hadoop.env` also forces `mapreduce.framework.name=local`,
which lets Hive execute its MapReduce jobs inside the HiveServer2 container
without a separate YARN cluster.

## Windows/MSYS caveat

Git Bash rewrites arguments that look like Unix paths. Docker commands therefore
run with:

```bash
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL='*'
```

`run.sh` sets both automatically. Without this, a container path such as
`/bda/attendance` is rewritten to a Windows path and HDFS reports
`No FileSystem for scheme: C`.

## What was verified

- `docker compose ... ps` shows all five containers running.
- HDFS accepted the upload: `Found 1 items`, `-rw-r--r-- ... 999647 /bda/attendance/attendance.csv`.
- Hive created `campus_attendance.attendance` as an EXTERNAL table.
- `SELECT COUNT(*)` returned **15,360**, matching the local CSV.
- All eight analytics queries executed and produced CSV output.
- An independent Python recomputation matched every Hive result (see
  `results/crosscheck_report.txt`).
- Real HDFS UI screenshots were captured with headless Chrome into
  `screenshots/`.

## Limitations recorded honestly

- Execution used containerised Hadoop/Hive, not a native Windows installation.
- No YARN cluster is used; Hive runs MapReduce in local mode inside the
  HiveServer2 container.
- The container images are older (Hadoop 2.7.4 / Hive 2.3.2) but are fully
  functional and use real HDFS and real HiveQL.
- Remaining manual steps (if a native Hadoop/Hive cluster is required) are in
  `README.md` and `RUNBOOK.md`.
