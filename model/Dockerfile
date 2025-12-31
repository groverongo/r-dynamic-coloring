FROM continuumio/miniconda3

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0

COPY environment.yml .
RUN conda env create -f environment.yml

ENV PATH="/opt/conda/envs/grids/bin:$PATH"

COPY main main

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
