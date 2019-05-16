FROM puckel/docker-airflow


CMD sudo mkdir -p ${AIRFLOW_HOME}/dags

COPY ./dags ${AIRFLOW_HOME}/dags/
COPY . .

# RUN pip install -r requirements.txt
RUN pip install --user -r requirements.txt