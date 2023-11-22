"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
# from airflow import DAG
# from airflow.operators.python_operator import PythonOperator
from airflow.decorators import dag, task
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
from pathlib import Path
import json
import requests
import jinja2
from docker.types import Mount



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

@dag('{AIT_NAME}_{AIT_VERSION}', default_args=default_args, schedule_interval=None, catchup=False, template_undefined=jinja2.Undefined)
def task_flow():

    @task(multiple_outputs=True)
    def pre_process(**context):
        print('start pre process.')

        if 'airflow_conf_file' not in context['dag_run'].conf:
            print('airflow_conf_file not exits in conf')
            return

        airflow_conf_file = context['dag_run'].conf['airflow_conf_file']
        with open(airflow_conf_file, encoding='utf-8') as f:
            conf_json = json.load(f)

        callback_url = conf_json['callback_url']

        input_json_dir = Path(conf_json['input_json_dir'])

        mount_volumes=[]
        for mount in conf_json['mounts']:
            src_path=mount['src_path']
            dst_path=mount['dst_path']
            
            if src_path == 'testbed_mount_volume_src':
                mount_volumes.append(Mount(source=src_path, target=dst_path, type="volume"))
            else:
                mount_volumes.append(Mount(source=src_path, target=dst_path, type="bind"))

        return {"mount_volumes": mount_volumes, "callback_url": callback_url, "input_json_dir": str(input_json_dir)}


    @task(trigger_rule=TriggerRule.ALL_DONE)
    def post_process(callback_url: str):
        print('start post process.')
        requests.post(callback_url)
 

    @task()
    def main_process(set_parms: dict, **context):
        
        mount_volumes = set_parms["mount_volumes"]
        input_json_dir = set_parms["input_json_dir"]
        callback_url = set_parms["callback_url"]

        run_dokcer = DockerOperator(
            task_id='main_process',
            image='{DOCKER_HOST_NAME}/{AIT_NAME}:{AIT_VERSION}',
            docker_url='unix://var/run/docker.sock',
            api_version='auto',
            auto_remove=True,
            mounts=mount_volumes,
            network_mode='bridge',
            mount_tmp_dir=False,
            command=input_json_dir,
            user='root'
        )

        run_dokcer.execute(context)

        return callback_url


    set_parms = pre_process()
    run_docker = main_process(set_parms)
    post_process(run_docker)

dag = task_flow()
