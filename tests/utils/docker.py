# tests/utils/docker.py

import pytest
from python_on_whales import docker
import time
import os
from loguru import logger
from tests.const import PROJECT_DIR

def is_container_ready(container):
    container.reload()
    return container.state.running

def wait_for_stable_status(container, stable_duration=3, interval=1):
    start_time = time.time()
    stable_count = 0
    while time.time() - start_time < stable_duration:
        if is_container_ready(container):
            stable_count += 1
        else:
            stable_count = 0
        
        if stable_count >= stable_duration / interval:
            return True
    
        time.sleep(interval)
    return False

def start_database_container():
    scripts_dir = os.path.abspath(f"{PROJECT_DIR}/scripts")
    container_name = "test-db"
    
    try:
        existing_container = docker.container.inspect(container_name)
        logger.info(f"Container '{container_name}' exists. Stopping and removing...")
        docker.container.stop(container_name)
        docker.container.remove(container_name)
        logger.info(f"Container '{container_name}' stopped and removed")
    except Exception as e:
        logger.info(f"Container '{container_name}' does not exist or could not be inspected: {e}")
        
    container_config = {
        "name": container_name,
        "image": "postgres:16.1-alpine3.19",
        "detach": True,
        "ports": {"35435:5432"},
        "environment": {
            "POSTGRES_USER": "postgres",
            "POSTGRES_PASSWORD": "postgres",
        },
        "volumes": [f"{scripts_dir}:/docker-entrypoint-initdb.d"],
        "network": 'fastapi-test-network'
    }
    
    container = docker.container.run(**container_config)
    
    while not is_container_ready(container):
        time.sleep(1)
        
    if not wait_for_stable_status(container):
        raise RuntimeError("Container did not stabilize within the specified time")
    
    return container