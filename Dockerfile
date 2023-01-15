# ffmpeg install stage
FROM amazonlinux:2022 as ffmpeg
RUN yum -y install wget
RUN yum -y install tar
RUN yum -y install xz
COPY install-ffmpeg.sh .
RUN ./install-ffmpeg.sh

# dependencies install stage
FROM amazon/aws-lambda-python:3.9 as dependencies
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Run Stage
FROM amazon/aws-lambda-python:3.9

COPY ./requirements.txt ./
COPY --from=dependencies /root/.cache /root/.cache

RUN pip install -r requirements.txt
COPY --from=ffmpeg /usr/local/bin/ffmpeg/ffmpeg /usr/bin/ffmpeg
COPY ./lambda_function.py /var/task/
COPY ./*.py /var/task/

CMD ["lambda_function.handler"]