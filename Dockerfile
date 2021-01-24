FROM ubuntu:18.04
WORKDIR /tmp/
RUN apt-get update \
    && apt-get install -y lib32z1 git make automake gdb gcc bc bcftools gawk graphviz \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/
ENV TARGET_FILE '/tmp/bin'
ENV ENV 'test'
COPY ./gdb/.conf/.gdbinit /root/.gdbinit
COPY ./gdb/target/test32 /tmp/bin
COPY ./gdb/gdb_scripts/ /tmp/gdb_scripts/
COPY ./gdb/.env.test /tmp/.env.test
COPY ./entrypoint.sh /tmp/entrypoint.sh
COPY ./gdb/Makefile /tmp/Makefile
CMD ["/bin/sh", "/tmp/entrypoint.sh", "&>", "result.txt"]
