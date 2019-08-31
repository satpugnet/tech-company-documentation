# K8S devenv

## Requirements

- Docker for desktop with **kubernetes** enabled
- `kubectl` (command line tool for kubernetes) - install it using `brew install kubernetes-cli`
- `skaffold` (command line tool for building k8s env locally) - install it using `brew install skaffold`

## Deploying

```bash
skaffold dev --cache-artifacts=true --port-forward
```