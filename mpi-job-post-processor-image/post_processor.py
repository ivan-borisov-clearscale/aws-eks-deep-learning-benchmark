# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import print_function
import json
import os
from kubernetes import client, config, watch
import yaml

def load_yaml_dict(file_name):
  # Step 1. Find MPI Job kubectl get -f /tmp/mpi-job.yaml -o name
  # Kubernetes Python SDK doesn't have api to get from file, parse from yaml instead
  with open(file_name, 'r') as stream:
    try:
      doc = yaml.load(stream)
    except yaml.YAMLError as exc:
      print(exc)

    namespace = doc.get('metadata').get('namespace', 'default')
    job_name = doc.get('metadata').get('name')
    return namespace, job_name

def dump_logs(namespace, job_name, output_dir):
  config.load_incluster_config()
  apiV1 = client.CoreV1Api()

  # Step 2. Find launcher pod
  # kubectl get pods -l mpi_job_name=mpi-job-custom,mpi_role_type=launcher -o name
  label_selector = 'mpi_job_name=' + job_name + "," + "mpi_role_type=launcher"
  pods = apiV1.list_namespaced_pod(namespace, label_selector=label_selector)

  # Step 3. Read pod logs - kubectl logs mpi-job-custom-launcher-rhvt4
  launcher_pod_name = pods.items[0].metadata.name
  #api_response = apiV1.read_namespaced_pod_log(launcher_pod_name, namespace, pretty='true', follow=True)

  w = watch.Watch()
  core_v1 = client.CoreV1Api()
  print('waiting for MPI launcher pod to started')
  for event in w.stream(apiV1.list_namespaced_pod,
                        namespace=namespace,
                        label_selector=label_selector):
    if event["object"].status.phase == "Running":
        w.stop()
        print('MPI launcher pod has started')
        break

  log_file = os.path.join(output_dir, launcher_pod_name)
  with open(log_file, 'w') as file_out:
    w = watch.Watch()
    for e in w.stream(apiV1.read_namespaced_pod_log, name=launcher_pod_name, namespace=namespace):
      print(e)
      print(e, file=file_out)

  return log_file

def run():
  config_dir = os.environ.get("KUBEBENCH_EXP_CONFIG_PATH")
  output_dir = os.environ.get("KUBEBENCH_EXP_OUTPUT_PATH")
  result_dir = os.environ.get("KUBEBENCH_EXP_RESULT_PATH")

  config_file = os.path.join(config_dir, "kf-job-manifest.yaml")
  result_file = os.path.join(result_dir, "result.json")

  namespace, job_name = load_yaml_dict(config_file)
  log_file = dump_logs(namespace, job_name, output_dir)


if __name__ == "__main__":
  run()