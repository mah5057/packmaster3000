FROM python:3.6.8

ADD . /packmaster3000

RUN apt-get update
RUN apt-get -y install gcc libsasl2-dev python-dev libldap2-dev libssl-dev curl
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get install -y nodejs
WORKDIR /packmaster3000/packmaster3000

RUN npm install -g @angular/cli@6.1.1
RUN npm install -g typescript
RUN npm install
RUN ng build --prod --aot=false --build-optimizer=false

WORKDIR /packmaster3000
RUN python -m pip install -r /packmaster3000/server/requirements.txt

EXPOSE 5000

CMD ["python", "/packmaster3000/server/packmaster.py"]

