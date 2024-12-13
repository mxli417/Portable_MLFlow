# Portable (dockerized) MLFlow remote tracking server setup

My version of a basic portable tracking server setup with all amentities to track and store experiments and models. Depends on MLFlow server wired up to a basic postgres DB and a basic minio instance. Requires mounted volumes to persist the tracking information and models. Should be buildable and deployable anywhere. Big props for the straightforward, simple and clean solution done by [Erik Dao](https://erikdao.com/about/).

## instructions

- copy the `.env-template` file or rename it to `.env`
  - set the right user names and pwds in the env vars - use discretion
  - for more professional undertakings and / or corporate use, consider [this](https://www.docker.com/blog/protecting-secrets-with-docker/)
- replace `ml-flow-bucket` with *your* selected minio-Bucket identifier
- replace / rewrite the volumes-section in the compose-file, see also the [docs](https://docs.docker.com/compose/)
- double check the docker-compose.yml s.t. every component has access to the relevant login/user information (else inspect the container logs)
- fire up the service: `docker-compose up -d --build`

## learnings

- The original docker-compose.yml settings from the original documentation on remote tracking / model artifact storage [here](https://mlflow.org/docs/latest/tracking/tutorials/remote-server.html) are faulty - minio is not reachable if it gets referred to by `localhost` in the container running the MLFlow server. This is explained in further detail [here](https://medium.com/@tuananhbk1996/facts-about-the-differences-between-localhost-127-0-0-1-and-host-docker-internal-fb1e1f8644f5#:~:text=in%20Docker%20Containers-,localhost%20and%20127.0.,running%20inside%20the%20same%20container.).
- The version done by Erik Dao [here](https://erikdao.com/machine-learning/production-ready-mlflow-setup-in-your-local-machine/) is also faulty because of: 
  - a very small error in the minio setup script - the server needs to spool up before a bucket is created. This is not included in the original version and leads to bucket creation failure - I fixed it after reading this [discussion](https://github.com/minio/mc/issues/3599)
  - the docker networking error (notwithstanding docker networking settings not shown) mentioned above
  - small, but security-relevant: original docs use env-vars sometimes but also hard coding the Postgres-DB access data in the docker-compose.yml, this is now rewritten to purely env vars
- Model registry staging is being deprecated [RFC:deprecating model registry stages](https://github.com/mlflow/mlflow/issues/10336) in favor of model version tags and model version aliases as well as promoting the use of MLFlow Authentication for different enviroments for different scenarios (think: dev, staging, prod).
  

## resources

- https://mlflow.org/docs/latest/tracking/tutorials/remote-server.html
- https://erikdao.com/machine-learning/production-ready-mlflow-setup-in-your-local-machine/
- https://min.io/
- https://min.io/docs/minio/linux/reference/minio-mc.html
- [Short bash script tutorial](https://www.youtube.com/watch?v=SPwyp2NG-bE)
- [Bash script tutorial](https://www.youtube.com/watch?v=tK9Oc6AEnR4)
