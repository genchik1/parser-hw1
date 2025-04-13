FROM python:3.12

WORKDIR /

COPY . .

RUN mkdir ./data
VOLUME ./data

RUN --mount=type=bind,target=./pyproject.toml,src=./pyproject.toml \
    --mount=type=bind,target=./uv.lock,src=./uv.lock \
    pip install --no-cache-dir uv==0.6.14 \
    && uv export --no-dev -o requirements.txt \
    && pip uninstall -y uv \
    && pip install --no-cache-dir -r requirements.txt \
    && rm requirements.txt

ENTRYPOINT ["python", "./cli.py"]
CMD [""]
