FROM puckel/docker-airflow


ARG AIRFLOW_VERSION=1.10.2
ARG AIRFLOW_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""

# COPY . /${AIRFLOW_HOME}
COPY /dags /usr/local/airflow/dags
COPY requirements.txt /usr/local/airflow


# USER airflow
WORKDIR ${AIRFLOW_HOME}
RUN pip install --user -r requirements.txt
# ENTRYPOINT ["/entrypoint.sh"]
# CMD ["webserver"] # set default arg for entrypoint