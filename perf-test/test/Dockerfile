From ubuntu:19.04
RUN apt -y update
RUN apt install -y python3 python3-pip
RUN pip3 install --user cryptography --force-reinstall

COPY . /app
WORKDIR /app

ENTRYPOINT [ "python3" ]
CMD ["run.py","laptop","docker"]

