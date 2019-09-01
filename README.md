# Tech documentation

A project to attempt to create a solid tool for documenting code internally for tech companies.

## Running the application

We use k8s locally. Setup the environment following the steps in [Setting up k8s locally](#Setting-up-k8s-locally).

K8s provides us many advantages such as:
- no need to install the dependencies locally, we fetch an image and make it run
- we run easily our databases such as mongo and redis using it
- we even run our local proxy client **smee** automatically thanks to k8s

There are 2 options when running the application (It is better when developing to choose **OPTION 2**, and use option 1
to check everything works before deploying).

**1. Run everything in k8s**

Pros:
- Easy to check if everything wires correctly
- Automatically updates files if they change

Cons:
- Logging is not as easy as having 2 terminal sessions where logs of frontend and backend are separate
- Containers often need to be recreated when making important changes to the global environment
- No debugging using intellij as the backend runs inside a container

**2. Use only k8s for external resources**

Pros:
- Easy to make change to frontend and backend as no container restart
- Debugging automatic using intellij as we run the app in a terminal window
- Logging is much clearer

## Setting up k8s locally

You will need to install:

- Docker for desktop with **kubernetes** enabled
- `kubectl` (command line tool for kubernetes) - install it using `brew install kubernetes-cli`
- `skaffold` (command line tool for building k8s env locally) - install it using `brew install skaffold`

## Running the full app inside k8s (Option 1)

```bash
MODE=ALL skaffold dev --cache-artifacts=true --port-forward
```

## Running the app using resources from k8s (Option 2)

```bash
MODE=APP_RESOURCES_ONLY skaffold dev --cache-artifacts=true --port-forward
```

In this case, we need to also spin up the frontend and the backend on our local machine.

Run the backend:

```bash
make backend
```

Run the frontend:

```bash
make frontend
```

## Check out the app

Visit http://localhost:8080/
