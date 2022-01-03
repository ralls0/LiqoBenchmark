# Test 1

For this test, we can play with a micro-services application provided by Google, which includes multiple cooperating services:

```bash
k create ns online-boutique
k apply -f https://raw.githubusercontent.com/Ralls0/LiqoBenchmark/ral/setup/kubernetes-manifests/kubernetes-manifests.yaml -n online-boutique
```

Once the demo application manifest is applied, you can observe the creation of the different pods:

```bash
k get pods -n online-boutique -o wide
```

And with the command `kubectl port-forward` you can forward the requests from your local machine (i.e. `http://localhost:8080`) to the frontend service:

```bash
kubectl port-forward -n online-boutique service/frontend-external 8080:80
```

Now you can analize the metrics of each pod by means of `Kubernetes Metrics Server`.

## Deploying the Kubernetes Metrics Server on a Cluster Using Kubectl

You can deploy the Kubernetes Metrics Server on clusters you create using Container Engine.

The Kubernetes Metrics Server is a cluster-wide aggregator of resource usage data. The Kubernetes Metrics Server collects resource metrics from the kubelet running on each worker node and exposes them in the Kubernetes API server through the Kubernetes Metrics API. Other Kubernetes add-ons require the Kubernetes Metrics Server, including:

- the Horizontal Pod Autoscaler (see Using the Kubernetes Horizontal Pod Autoscaler)
- the Vertical Pod Autoscaler (see Using the Kubernetes Vertical Pod Autoscaler)

To deploy the Kubernetes Metrics Server on a cluster you've created with Container Engine for Kubernetes:

1. In a terminal window, deploy the Kubernetes Metrics Server by entering:
  
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/<version-number>/components.yaml
```

where <version-number> is the Kubernetes Metrics Server version that you want to deploy. For example, v0.5.2.

2. Confirm that the Kubernetes Metrics Server has been deployed successfully and is available by entering:

```bash
kubectl get deployment metrics-server -n kube-system
```

> NOTE: In the case of the deployment doesn't start, and into the logs you show the error: Failed to scrape node err ... x509: cannot validate certificate for ... because it doesn't contain any IP SANs" node="cluster1-control-plane". So, you should add `- --kubelet-insecure-tls` under the args row.