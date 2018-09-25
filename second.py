import boto3
import json
import twitter
import wikipediaapi


def main():
    # Used to test in local
    tweet("toto", "popo")


def tweet(event, context):
    sqs = boto3.client('sqs')
    queue = sqs.get_queue_url(QueueName='YOUR-SQS')
    response = sqs.receive_message(
        QueueUrl=queue["QueueUrl"],
        AttributeNames=['All'],
        MessageAttributeNames=[
            'string',
        ],
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )
    api = twitter.Api(consumer_key='CONSUMER-KEY',  # BotAPiKey
                      consumer_secret='CONSUMER-SECRET',  # BotAPiKey
                      access_token_key='BOT-TOKEN',  # YourApiKey
                      access_token_secret='BOT-TOKEN-SECRET')  # YourApiKey
    villeJson = json.loads(response["Messages"][0]["Body"])
    wiki_wiki = wikipediaapi.Wikipedia('fr')
    page_py = wiki_wiki.page(villeJson["nom"])
    to_display = "Nom: " + villeJson["nom"] + "\n" + "Code Postal: " + villeJson["codesPostaux"][0] + "\n" "Population: " + str(
        villeJson["population"]) + "\n \n"

    to_display += page_py.summary[0:(280 - len(to_display) - len(page_py.fullurl) - 5)] + "...\n" + page_py.fullurl
    status = api.PostUpdate(to_display)
    if status != "":
        responseDel = sqs.delete_message(
            QueueUrl=queue["QueueUrl"],
            ReceiptHandle=response["Messages"][0]["ReceiptHandle"]
        )
        print("SUCCESS")
    else:
        print("FAILED")


if __name__ == '__main__':
    main()
