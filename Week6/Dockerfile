FROM python:3.8

#_ INSTALL CMAKE
RUN apt-get update && \
	apt-get --yes install cmake

#_ INSTALL MGCLIENT
RUN apt-get install -y git cmake make gcc g++ libssl-dev && \
	git clone https://github.com/memgraph/mgclient.git /mgclient && \
	cd mgclient && \
	git checkout dd5dcaaed5d7c8b275fbfd5d2ecbfc5006fa5826 && \
	mkdir build && \
	cd build && \
	cmake .. && \
	make && \
	make install

# #_ INSTALL PYMGCLIENT
# RUN git clone https://github.com/memgraph/pymgclient /pymgclient && \
#     cd pymgclient && \
#     python3 setup.py build && \
#     python3 setup.py install

#_ INSTALL PACKAGES
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY Week6_Assignment.py /app/Week6_Assignment.py
WORKDIR /app

ENV FLASK_ENV=development
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTH-8

CMD ["python3", "Week6_Assignment.py"]