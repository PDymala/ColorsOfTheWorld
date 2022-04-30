from google.cloud import secretmanager


def access_secret_version(secret_id, version_id="latest"):

    client=secretmanager.SecretManagerServiceClient()

    name = f"{secret_id}/versions/{version_id}"

    response = client.access_secret_version(name=name)

    return response.payload.data.decode('UTF-8')