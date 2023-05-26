
const aws = require('aws-sdk');

{%- set lambda = asyncapi.ext('x-quantum-awslambda') %}
const s3 = new aws.S3({ apiVersion: '2006-03-01', region: '{{lambda.region}}' });
exports.handler = function (event, context, callback) {
    const mqtt = require('mqtt');
    var client = mqtt.connect('{{ asyncapi.server(params.server).protocol() }}://{{ asyncapi.server(params.server).url() |  replaceServerVariablesWithValues(asyncapi.server(params.server).variables()) | stripProtocol  }}', { clientId: "publisher" });
    client.on("connect", function () {
        getS3Data(event, client);
    });

}



async function getS3Data(event, client) {
    await s3.getObject({
        Bucket: event.Records[0].s3.bucket.name,
        Key: decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' '))
    }).promise().then(data => {
        var fileData = data.Body.toString('utf-8');
        client.publish("{{lambda.channel}}", JSON.stringify({ data: fileData }));
        client.end();
    })

};





