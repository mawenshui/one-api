FROM node:16 AS builder

WORKDIR /web
COPY ./VERSION .

# Only copy the active theme directory to speed up build.
# Currently active theme is "berry" (see docker-compose.fork.yml THEME env).
# Default / air themes are NOT needed at runtime — one-api only serves the active theme.
COPY ./web/berry ./berry

RUN npm install --prefix /web/berry

# Build the berry theme. The npm run build script ends with "mv -f build ../build/berry"
# which fails in the container (../build dir doesn't exist yet) — we just build and copy manually.
RUN DISABLE_ESLINT_PLUGIN='true' REACT_APP_VERSION=$(cat ./VERSION) npm run build --prefix /web/berry || true

# Manual staging (npm script's mv may have failed; build artifacts live in /web/berry/build).
RUN mkdir -p /web/build/berry && cp -r /web/berry/build/. /web/build/berry/

FROM golang:alpine AS builder2

RUN apk add --no-cache \
    gcc \
    musl-dev \
    sqlite-dev \
    build-base

ENV GO111MODULE=on \
    CGO_ENABLED=1 \
    GOOS=linux

WORKDIR /build

ADD go.mod go.sum ./
RUN go mod download

COPY . .
COPY --from=builder /web/build ./web/build

RUN go build -trimpath -ldflags "-s -w -X 'github.com/songquanpeng/one-api/common.Version=$(cat VERSION)' -linkmode external -extldflags '-static'" -o one-chat

FROM alpine:latest

RUN apk add --no-cache ca-certificates tzdata

COPY --from=builder2 /build/one-chat /

EXPOSE 3000
WORKDIR /data
ENTRYPOINT ["/one-chat"]
