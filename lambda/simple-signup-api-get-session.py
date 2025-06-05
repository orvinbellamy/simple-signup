import json
import logging
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

	logger.info("FULL EVENT: " + json.dumps(event, default=str))
	
	username = event["pathParameters"]["username"]
	raw_session_id = event["pathParameters"]["id"]

	# session_id = int(raw_id)
	session_id = f"SESSION#{raw_session_id}"

	dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
	table = dynamodb.Table("AppData")

	try:
		# This doesn't work because session_id is not the PK, so we need to use GSI
		# resp = TABLE.get_item(Key={"session_id": session_id})

		resp = table.get_item(
			Key={
				'PK': username,
				'SK': session_id
			}
		)

		if "Item" not in resp:
			return {
				"statusCode": 404,
				"body": json.dumps({"message": "Session not found"})
			}
		else:
			
			session_data = resp.get('Item')

			return {
				"statusCode": 200,
				'headers': {
					'Cache-Control': 'no-store',
					'Pragma': 'no-cache'
				},
				"body": json.dumps(session_data, default=str),
				"headers": {"Content-Type": "application/json"}
			}
	except ClientError as e:
		return {
			"statusCode": 500,
			"body": json.dumps({"error": e.response["Error"]["Message"]})
		}