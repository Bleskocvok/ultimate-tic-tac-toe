FROM python:3.10

WORKDIR /app

COPY --chown=1001 . .

RUN pip install -r requirements.txt

USER 1001

ENTRYPOINT [ "python3", "-m", "src.bot" ]
