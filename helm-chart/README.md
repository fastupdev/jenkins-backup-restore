## Introduction
 helm-chart Chart is a generic helm chart for the jenkins-backup-restore-cli to deploy to kubernetes. 

## Prerequisites
- Helm 3.0.2 or higher
- Download the repository to install the chart

> Note: As of right now the chart is not hosted in any chart repo, feel free to build a chart and 
>install it.

## Chart Details
This Helm Chart includes the following implementations,
- Deploy a pod with the jenkins-backup-restore-cli installed in it.
- Mount a volume in the pod if need a local-backup and store it in a persistent volume.

## Installing the Chart

#### **Base Installation**
Run the following command to install the helm-chart.
```
helm upgrade --install <release-name> 
      --atomic \
      --force \
      --kubeconfig <path-to-kubeconfig> \
      --set image.imageRepository=<image-repository> \
      --set image.imageName=<image-name> \
      --set image.imageTag=<image-tag>
      --values ${values_file} \
      --namespace <jenkins-namespace>
```

## Configuration
#### **Volumes**
The following snippet should be added to the values.yaml file to, to create a backup into a persistent volume or restore an already created backup in a persistent volume.
```
volumes:
  volumeName: jenkins-home
  persistentVolumeClaimName: <persistentVolumeClaimName>
  mountPath: /tmp
```

- `volumeName` name of the volume
- `persistentVolumeClaimName` the persistent volume claim name of the jenkins.
- `mountPath` the path where the volume to mount

> Note: For the persistentVolumeClaimName, provide the existing jenkins persistentVolumeClaimName.


## Uninstalling the Chart
To uninstall the helm chart, run the following command
```
helm uninstall <release-name>
```
