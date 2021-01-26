FROM ubuntu:18.04
WORKDIR /tmp/
RUN apt-get update \
    && apt-get install -y lib32stdc++6 lib32z1 libc6-i386 git make gdb gcc gawk  \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/
ENV TARGET_FILE '/tmp/bin'
ENV ENV 'docker'
COPY ./gdb/.conf/.gdbinit /root/.gdbinit
COPY ./gdb/target/test /tmp/bin
COPY ./gdb/gdb_scripts/ /tmp/gdb_scripts/
COPY ./.env.docker /tmp/.env
COPY ./entrypoint.sh /tmp/entrypoint.sh
COPY ./gdb/Makefile /tmp/Makefile
CMD ["/bin/sh", "/tmp/entrypoint.sh", "&>", "result.txt"]
