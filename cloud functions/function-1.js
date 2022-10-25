const functions = require('@google-cloud/functions-framework');
const compute = require('@google-cloud/compute');

const projectId = '[PROJECT_ID]';
const zone = '[ZONE]';
const instanceName = '[INSTANCE_NAME]'

async function secondInstance(){
  const instancesClient = new compute.InstancesClient();

  const [response] = await instancesClient.start({
    project: projectId,
    zone,
    instance: instanceName,
  });
  let operation = response.latestResponse;
  const operationsClient = new compute.ZoneOperationsClient();

  // Wait for the operation to complete.
  while (operation.status !== 'DONE') {
    [operation] = await operationsClient.wait({
      operation: operation.name,
      project: projectId,
      zone: operation.zone.split('/').pop(),
    });
  };

  console.log('Instance started.');
}

async function handleStartInstance(req,res) {
  await secondInstance().then();
  res.status(200).send('Minecraft Server Started');
};

functions.http('startInstance',handleStartInstance);
