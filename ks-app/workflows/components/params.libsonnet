{
  global: {},
  components: {
    // Component-level parameters, defined initially from 'ks prototype use ...'
    // Each object below should correspond to a component in the components/ directory
    workflows: {
      s3ResultPath: 's3://poc-embark-dl-benchmark/benchmark-result/',
      s3DatasetPath: 's3://poc-embark-dl-benchmark/data/imagenet/',
      clusterConfig: 's3://poc-embark-dl-benchmark/config/cluster_config.yaml',
      experiments: [{
        experiment: 'experiment-20190415-01',
        trainingJobConfig: 's3://poc-embark-dl-benchmark/config/benchmark/mpi-resnet50synth.yaml',
        trainingJobPkg: 'mpi-job@v0.7-branch',
        trainingJobPrototype: 'mpi-job-custom',
        trainingJobRegistry: 'https://github.com/ivan-borisov-clearscale/kubeflow/tree/v0.7-branch/kubeflow',
      }],
      githubSecretName: 'github-token',
      githubSecretTokenKeyName: 'GITHUB_TOKEN',
      image: 'seedjeffwan/benchmark-runner:20190424',
      name: 'poc-embark-dl-benchmark',
      namespace: 'default',
      nfsVolume: 'benchmark-pv',
      nfsVolumeClaim: 'benchmark-pvc',
      region: 'us-east-1',
      trainingDatasetVolume: 'dataset-claim', # should pass to storage pvc name
      s3SecretName: 'aws-secret',
      s3SecretAccesskeyidKeyName: 'AWS_ACCESS_KEY_ID',
      s3SecretSecretaccesskeyKeyName: 'AWS_SECRET_ACCESS_KEY',
      storageBackend: 'fsx',
      kubeflowRegistry: 'https://github.com/ivan-borisov-clearscale/kubeflow/tree/v0.7-branch/kubeflow'
    },
  },
}
