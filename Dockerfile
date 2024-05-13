FROM python:3.12
ARG USERNAME=worker
ARG USER_UID=1000
ARG USER_GID=$USER_UID

LABEL ch.yax.teal.url="https://github.com/rueedlinger/teal"

WORKDIR /usr/src/app

# supported tesseract languages https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html
RUN groupadd --gid $USER_GID $USERNAME &&\
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_x86_64  &&\
    chmod +x /usr/local/bin/dumb-init && \
    apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get install -y tesseract-ocr-deu && \
    apt-get install -y tesseract-ocr-fra && \
    apt-get install -y tesseract-ocr-ita && \
    apt-get install -y tesseract-ocr-eng && \
    apt-get install -y tesseract-ocr-por && \
    apt-get install -y tesseract-ocr-spa && \
    apt-get install -y poppler-utils && \
    apt-get install -y ocrmypdf && \
    apt-get install -y ghostscript python3-tk && \
    apt-get install -y libgl1 && \
    apt-get install -y ocrmypdf && \
    apt-get --no-install-recommends install -y libreoffice && \
    apt-get install -y default-jre-headless libreoffice-java-common jodconverter

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY log_conf.yaml ./
COPY run.sh ./
RUN chmod 755 run.sh

RUN mkdir /usr/src/app/teal
COPY teal ./teal

USER $USERNAME
# Runs "/usr/bin/dumb-init -- /my/script --with --args"
ENTRYPOINT ["/usr/local/bin/dumb-init", "--"]
CMD ["/usr/src/app/run.sh"]