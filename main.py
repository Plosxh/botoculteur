import csv
import requests
import json
from urllib.parse import urljoin
import boto3


def main():
    sqs = boto3.client(
        'sqs',
        # Hard coded strings as credentials, not recommended.
        aws_access_key_id='AWS-ACCESS-KEY',
        aws_secret_access_key='AWS-SECRET-KEY',
        region_name='AWS-REGION'
    )
    queue = sqs.get_queue_url(QueueName='YOUR-SQS')
    counter = 0
    with open('laposte_hexasmal.csv', newline='') as csvfile:


        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            counter += 1
            if counter != 1:
                ville = request_ville(row[0])
                try:
                    if ville:
                        ville_json = json.dumps(ville)
                        response = sqs.send_message(QueueUrl=queue["QueueUrl"], MessageBody=ville_json, DelaySeconds=123)
                    else:
                        pass
                except json.decoder.JSONDecodeError:
                    print(counter)
                    print(ville)
    print("finished with : " + str(counter) + " cities")


def request_ville(insee):
    # Get Cities information
    url = "https://geo.api.gouv.fr/communes/" + str(insee) + "?fields=nom,code,codesPostaux,codeDepartement,codeRegion,population&format=json&geometry=centre"
    response = requests.get(url)
    if response.status_code != 200:
        print(response.status_code)
        return ""
    else:
        return response.json()




if __name__ == '__main__':
    main()
