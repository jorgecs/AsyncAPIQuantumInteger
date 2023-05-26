# {{ asyncapi.info().title() }}

{{ asyncapi.info().description() | safe }}

## Running the server

1. Install dependencies
    ```sh
    npm i
    ```
{%- if params.securityScheme and (asyncapi.server(params.server).protocol() === 'kafka' or asyncapi.server(params.server).protocol() === 'kafka-secure') and asyncapi.components().securityScheme(params.securityScheme).type() === 'X509' %}
1. (Optional) For X509 security provide files with all data required to establish secure connection using certificates. Place files like `ca.pem`, `service.cert`, `service.key` in the root of the project or the location that you explicitly specified during generation.
{%- endif %}
1. Start the server with default configuration
    ```sh
    npm start
    ```
1. (Optional) Start server with secure production configuration
    ```sh
    NODE_ENV=production npm start
    ```

{%- if asyncapi.ext('x-awslambda') %}
In order to create your lambda function on AWS you need to install the dependencies on a node_modules folder inside src/api/lambda.
1. Go to src/api/lambda
    ```sh
    cd src/api/lambda
    ```
2. Install dependencies
    ```sh
    npm i
    ```
{%- endif %}

In order to invoke the quantum services using this template, you also need to have a .aws folder with your credentials and configuration in your home directory, as it is explained here https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

> NODE_ENV=production relates to `config/common.yml` that contains different configurations for different environments. Starting server without `NODE_ENV` applies default configuration while starting the server as `NODE_ENV=production npm start` applies default configuration supplemented by configuration settings called `production`.