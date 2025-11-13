FROM alpine:3.22

ARG GID=1000
ARG UID=1000

RUN apk add graphviz make bash curl pandoc-cli texlive-xetex texmf-dist-latexextra
RUN apk add font-dejavu


RUN mkdir /home/builder
RUN chown "$GID:$UID" /home/builder

USER "$GID:$UID"
ENV HOME=/home/builder