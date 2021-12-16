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

