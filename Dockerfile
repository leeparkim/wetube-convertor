# Builder Stage
FROM amazonlinux:2022 as builder
RUN yum -y install wget
RUN yum -y install tar
RUN yum -y install xz
COPY install-ffmpeg.sh .
RUN ./install-ffmpeg.sh

# Run Stage
FROM amazon/aws-lambda-python:3.9
COPY --from=builder /usr/local/bin/ffmpeg/ffmpeg /usr/bin/ffmpeg
COPY ./lambda_function.py /var/task/

CMD ["lambda_function.handler"]