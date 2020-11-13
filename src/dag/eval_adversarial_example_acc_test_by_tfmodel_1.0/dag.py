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
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

with DAG('eval_adversarial_example_acc_test_by_tfmodel_1.0', default_args=default_args, schedule_interval=None, catchup=False) as dag:
    def pre_process(**context):
        print('start pre process.')

        if 'airflow_args_file' not in context['dag_run'].conf:
            print('airflow_args_file not exits in conf')
            return

        if 'callback_url' not in context['dag_run'].conf:
            print('callback_url not exits in conf')
            return

        airflow_args_file = context['dag_run'].conf['airflow_args_file']
        with open(airflow_args_file, encoding='utf-8') as f:
            args_json = json.load(f)

        mount_volumes=[]
        for mounts in args_json['mounts']:
            mount_volumes.append('{}:{}'.format(mounts['src_path'], mounts['dst_path']))

        callback_url = context['dag_run'].conf['callback_url']

        context['ti'].xcom_push(key='mount_volumes', value=mount_volumes)
        context['ti'].xcom_push(key='callback_url', value=callback_url)

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
        image='127.0.0.1:5500/eval_adversarial_example_acc_test_by_tfmodel:1.0',
        docker_url='unix://var/run/docker.sock',
        api_version='auto',
        auto_remove=True,
        # environment={
        #     'AF_EXECUTION_DATE': "{{ ds }}",
        #     'AF_OWNER': "{{ task.owner }}"
        # },
        #command='/bin/bash -c \'echo "TASK ID (from macros): {{ task.task_id }} - EXECUTION DATE (from env vars): $AF_EXECUTION_DATE"\'',
        network_mode='bridge',
        # volumes=['/C/testbed_mount_volume/ip/job_args:/usr/local/qai/args',
        #          '/C/testbed_mount_volume/ip/job_result:/usr/local/qai/result',
        #          '/C/testbed_mount_volume/ip/dummyInventory:/usr/local/qai/inventory']
        #volumes="{{ ti.xcom_pull(task_ids='pre_process', key='mount_volumes') }}"
    )

    t1 >> t2 >> t3
