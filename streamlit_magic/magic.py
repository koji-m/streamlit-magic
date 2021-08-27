import json
import subprocess

import google.cloud.storage.client as gcs
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)


@magics_class
class StreamlitMagics(Magics):
    @cell_magic
    def streamlit_config(self, line, cell):
        conf = json.loads(cell)
        self._project_id = conf['project_id']
        self._bucket_name = conf['bucket_name']
        self._blob_prefix = conf.get('blob_prefix', 'streamlit_files/')
        self._cloud_run_region = conf.get('cloud_run_region', 'us-central1')
        self._image_name = conf['image_name']

    @cell_magic
    def streamlit_deploy(self, line, cell):
        # deploy streamlit file to GCS
        service_name = line.split(' ')[0]
        client = gcs.Client(self._project_id)
        bucket = client.get_bucket(self._bucket_name)
        blob = bucket.blob(f'{self._blob_prefix}{service_name}.py')
        res = blob.upload_from_string(cell)
        print('The code is successfully deployed to GCS.')

        # check Cloud Run service and delete the service if exists
        proc = subprocess.run(
            ['gcloud', 'run', 'services', 'describe', service_name,
             '--region', self._cloud_run_region, '--format', 'json',
             '--project', self._project_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if proc.returncode == 0:
            proc = subprocess.run(
                ['gcloud', 'run', 'services', 'delete', service_name,
                 '--region', self._cloud_run_region, '--project', self._project_id],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f'Cloud Run service already exists. Deleted.')

        # deploy Cloud Run service
        proc = subprocess.run(
            ['gcloud', 'run', 'deploy', service_name, '--image', f'gcr.io/{self._project_id}/{self._image_name}:latest',
             '--region', self._cloud_run_region, '--allow-unauthenticated', '--args',
             f'{self._project_id},{service_name},{self._bucket_name},{self._blob_prefix}{service_name}.py',
             '--project', self._project_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if proc.returncode != 0:
            raise Exception(proc.stderr.decode('utf-8'))

        # get the URL of deployed Cloud Run service
        proc = subprocess.run(
            ['gcloud', 'run', 'services', 'describe', service_name,
             '--region', self._cloud_run_region, '--format', 'json',
             '--project', self._project_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if proc.returncode != 0:
            raise Exception(proc.stderr.decode('utf-8'))

        url = json.loads(proc.stdout.decode('utf-8'))['status']['url']

        print(f'Cloud Run service is successfully deployed.\n{url}')


def load_ipython_extension(ipython):
    ipython.register_magics(MyMagics)

