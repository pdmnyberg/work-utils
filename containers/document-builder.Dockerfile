FROM alpine:3.22

ARG GID=1000
ARG UID=1000

RUN apk add graphviz make bash

USER "$GID:$UID"