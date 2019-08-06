FROM python:3.5.7-jessie
RUN apt-get update && apt-get -y install libsasl2-dev python-dev libldap2-dev libssl-dev redis-server
WORKDIR /nominate_ur_bee
COPY . /nominate_ur_bee	
RUN pip install -r requirements.txt
EXPOSE 3003
CMD ["sh","/nominate_ur_bee/entrypoint.sh"]