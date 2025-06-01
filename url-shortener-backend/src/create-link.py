import os, json, random, string, boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])
BASE_URL = os.environ["BASE_URL"]

def random_slug(k=6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=k))

def lambda_handler(event, context):
    body = json.loads(event["body"] or "{}")
    long_url = body.get("url")
    if not long_url:
        return {"statusCode": 400, "body": "url is required"}
    
    # ensure uniqueness
    for _ in range(5):
        slug = random_slug()
        try:
            table.put_item(
                Item = {"slug": slug, "long_url": long_url, "clicks" : 0},
                ConditionExpression="attribute_not_exists(slug)"
            )
            break
        except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
            continue
        
    else:
        return {"statusCode": 500, "body": "Failed to geberate slug"}
    
    return {
        "statusCode": 201,
        "headers": {"Content-Type": "aplication/json"},
        "body": json.dumps({"short_url": f"{BASE_URL}/{slug}"})
    }
    