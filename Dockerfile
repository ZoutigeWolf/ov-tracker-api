FROM mambaorg/micromamba:0.27.0

COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yaml /tmp/environment.yaml

RUN micromamba install -y -n base -f /tmp/environment.yaml && \
    micromamba clean --all --yes

WORKDIR /code

COPY . /code

USER root

RUN mkdir -p /code/data/buffers

RUN chown -R $MAMBA_USER /code/data/buffers

USER $MAMBA_USER

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]