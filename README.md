# Dependencies

Kubernetes cli for mac
```
brew install kubectl
```

Small kubernetes engine that runs inside docker
```
brew install kind
```

optional - kubernetes management tool, good for visualization, logs etc
```
brew install k9s
```

# Setup


To simplify the configuration, the project folder must be called
`instances-management`, otherwise the built images will have different names
from the automated make commands.

```
git clone https://github.com/luigibertaco/spike-k8s-instances-mngmt.git instances-management
cd instances-management
kind create cluster --config deploy/cluster.yaml
make setup
```

# Usage

- http://localhost/tasks
  - shows tasks history
- http://localhost/pods
  - lists all pods on the cluster
- http://localhost/pod/new/team-a
  - creates a deployment for team-a worker (tier 1 - 1 replica)
- http://localhost/pod/new/team-b/2
  - creates a deployment for team-b worker (tier 2 - 2 replicas)
- http://localhost/tasks/new/team-a
  - creates a task to be processed by team-a's workers
- http://localhost/tasks/new/team-b
  - creates a task to be processed by team-b's workers
- http://localhost/pod/update/team-b/1
  - updates team-b to tear-1 (1 replica)
- http://localhost/pod/delete/team-a
  - delete team-a deployment and workers
