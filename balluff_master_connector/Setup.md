Example run command:
docker run --name balluff_master_connector_$DEVICE_NAME  --env MASTER_IP --env QUEUE_DICT --env DEVICE_NAME --network iotbridge_webnet -d balluff_master_connector 
Remember to set up the env variable