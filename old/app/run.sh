cd fastapi_microservice &&\
conda activate mlops_hw_env && \
uvicorn main:app --host 0.0.0.0 --port 8080