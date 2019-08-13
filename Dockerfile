FROM python:3

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN curl https://cli-assets.heroku.com/install.sh | sh
COPY . /src/
WORKDIR /src
CMD ["bash"]
