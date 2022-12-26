#!/bin/bash
cd fastapi_microservice
# chmod 777 run.sh
# ./run.sh
conda activate mlops_hw_env && \
uvicorn main:app --host 0.0.0.0 --port 8080
# echo 123
# # enable conda for this shell
# ./opt/conda/etc/profile.d/conda.sh


# # activate the environment
# conda activate mlops_hw_env

# # exec the cmd/command in this process, making it pid 1
# exec "$@"
