FROM amazon/aws-lambda-python:3.9
RUN yum -y install wget
RUN yum -y install tar
RUN yum -y install xz
COPY install-ffmpeg.sh .
RUN ./install-ffmpeg.sh
COPY ./lambda_function.py /var/task/

CMD ["lambda_function.handler"]