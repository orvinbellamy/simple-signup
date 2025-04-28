import json
import logging
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

	logger.info("FULL EVENT: " + json.dumps(event, default=str))
	
	raw_id = event["pathParameters"]["id"]

	session_id = int(raw_id)

	dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
	table = dynamodb.Table("AppData")

	try:
		# This doesn't work because session_id is not the PK, so we need to use GSI
		# resp = TABLE.get_item(Key={"session_id": session_id})

		resp = table.query(
			IndexName="idx_session_id",  # whatever name you gave the GSI
			KeyConditionExpression=Key("session_id").eq(session_id)
		)
		if "Items" not in resp:
			return {
				"statusCode": 404,
				"body": json.dumps({"message": "Session not found"})
			}
		else:
			
			session_data = resp['Items'][0]

			return {
				"statusCode": 200,
				"body": json.dumps(session_data, default=str),
				"headers": {"Content-Type": "application/json"}
			}
	except ClientError as e:
		return {
			"statusCode": 500,
			"body": json.dumps({"error": e.response["Error"]["Message"]})
		}