import os, boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def handler(event, context):
    slug = event["pathParameters"]["slug"]
    item = table.get_item(Key={"slug": slug}).get("Item")
    if not item:
        return {"statusCode": 404, "body": "Not found"}

    # Increment click counter (fire-and-forget)
    table.update_item(
        Key={"slug": slug},
        UpdateExpression="SET clicks = if_not_exists(clicks, :zero) + :one",
        ExpressionAttributeValues={":one": 1, ":zero": 0},
    )

    return {
        "statusCode": 301,
        "headers": {"Location": item['long_url']}
    }
