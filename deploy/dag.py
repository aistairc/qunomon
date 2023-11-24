"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
from pathlib import Path
import shutil
import json
import requests


class DockerOperatorEx(DockerOperator):
    def execute(self, context):
        volumes = context['ti'].xcom_pull(key='mount_volumes')
        self.volumes.extend(volumes)
        super().execute(context)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2015, 6, 1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "provide_context": True,
    "retry_delay": timedelta(minutes=5)
}

with DAG('dev_template_remote_docker-airc_0.1', default_args=default_args, schedule_interval=None, catchup=False) as dag:

    def pre_process(**context):
        print('start pre process.')

        if 'airflow_conf_file' not in context['dag_run'].conf:
            print('airflow_conf_file not exits in conf')
            return

        airflow_conf_file = context['dag_run'].conf['airflow_conf_file']
        with open(airflow_conf_file, encoding='utf-8') as f:
            conf_json = json.load(f)

        mount_volumes=[]
        for mounts in conf_json['mounts']:
            mount_volumes.append('{}:{}'.format(mounts['src_path'], mounts['dst_path']))

        callback_url = conf_json['callback_url']

        input_json_dir = Path(conf_json['input_json_dir'])

        context['ti'].xcom_push(key='mount_volumes', value=mount_volumes)
        context['ti'].xcom_push(key='callback_url', value=callback_url)
        context['ti'].xcom_push(key='input_json_dir', value=input_json_dir)

    def post_process(**context):
        print('start post process.')
        callback_url = context['ti'].xcom_pull(key='callback_url')
        requests.post(callback_url)

    t1 = PythonOperator(
        task_id='pre_process',
        python_callable=pre_process,
        dag=dag
    )

    t3 = PythonOperator(
        task_id='post_process',
        python_callable=post_process,
        trigger_rule=TriggerRule.ALL_DONE, # error発生時でも必ず実行する
        dag=dag
    )

    t2 = DockerOperatorEx(
        task_id='main_process',
        image='qunomon/dev_template_remote_docker-airc:0.1',
        docker_url='unix://var/run/docker.sock',
        api_version='auto',
        auto_remove=True,
        command="{{ ti.xcom_pull(task_ids='pre_process', key='input_json_dir') }}",
        network_mode='bridge',
    )

    t1 >> t2 >> t3
