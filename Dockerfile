FROM fedora:33

RUN dnf install -y \
    python3 \
    python3-pip \
    && dnf clean all

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY app.py /app/app.py