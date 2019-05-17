FROM puckel/docker-airflow


ARG AIRFLOW_VERSION=1.10.2
ARG AIRFLOW_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""

COPY /dags /usr/local/airflow/dags
COPY requirements.txt /usr/local/airflow


WORKDIR ${AIRFLOW_HOME}
RUN pip install --user -r requirements.txt
