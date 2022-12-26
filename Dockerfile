FROM continuumio/anaconda3
# RUN mkdir -p /app/fastapi_microservice
ADD ./ /app/
# ADD ./Dockerfile /app/
# ADD ./README.md /app/
# ADD ./requirements.txt /app/
WORKDIR /app/

ENV fastapi_host=0.0.0.0
ENV fastapi_port=8080
ENV postgress_host=172.19.0.2
ENV postgress_password=password
ENV postgress_user=postgres
ENV postgress_db=test

# RUN pip install -r requirements.txtt

# sudo docker run -it --rm -v docker_temp:/app/docker_temp -p 8888:8888 -p 8080:8080  --name=fastapi_microservice mlops_hw

# # Install conda env and go into it
# RUN . /root/.bashrc && \
#     conda init bash && \
#     conda env create -f fastapi_microservice/environment.yml &&\
#     # conda create --name mlops_hw_env python=3.9 && \ FASTWAY
#     conda activate mlops_hw_env

# # Print is everything alright
# RUN conda env list

# RUN python -v

# ENTRYPOINT
# # Python program to run in the container
# COPY run.py .
# ENTRYPOINT ["conda", "run", "-n", "env", "python", "run.py"]

# BUILD DOCKER
# sudo docker build . -t mlops_hw

# RUN DOCKER
# sudo docker run -it mlops_hw



# ADD ./entrypoint.sh /app/entrypoint.sh
# RUN chmod +x ./entrypoint.sh




# ENTRYPOINT ["./entrypoint.sh"]

# 
# Trash
# RUN conda env create -f fastapi_microservice/environment_small.yml
# RUN conda env create -f fastapi_microservice/environment.yml

# Activate conda env
# RUN conda activate mlops_hw_env
# SHELL ["conda", "run", "-n", "mlops_hw_env", "/bin/bash", "-c"]


# ENTRYPOINT ["tail", "-f", "/dev/null"]
# RUN sh
# RUN conda activate mlops_hw_env
# RUN uvicorn main:app --reload

