FROM python:3.8

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ../src/ ./src/
COPY ../lib/ ./lib/
COPY ../resources/ ./resources/

CMD ["python", "-m", "src.benchmark.__init__", "./resources/teams", "./resources/games/"]
