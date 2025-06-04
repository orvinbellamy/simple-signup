import json
import logging
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

	logger.info("FULL EVENT: " + json.dumps(event, default=str))
	
	# 1) Extract the host’s Cognito user sub from the authorizer
	username = event['pathParameters']['username']

	if not username:
		logger.error("Username is missing in path parameters")
		return {
			"statusCode": 400,
			"body": json.dumps({"message": "Username is required"}),
			"headers": {"Content-Type": "application/json"}
		}

	logger.info(f"Username: {username}")

	dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
	table = dynamodb.Table("AppData")

	try:
		# This doesn't work because session_id is not the PK, so we need to use GSI
		# resp = TABLE.get_item(Key={"session_id": session_id})

		resp = table.query(
			KeyConditionExpression=Key('PK').eq(username) & Key('SK').begins_with('SESSION#')
		)

		if "Items" not in resp:
			return {
				"statusCode": 404,
				"body": json.dumps({"message": "No session found"}),
				"headers": {"Content-Type": "application/json"}
			}
		else:
			
			session_data = resp['Items']

			return {
				"statusCode": 200,
				"body": json.dumps(session_data, default=str),
				"headers": {"Content-Type": "application/json"}
			}
	except ClientError as e:
		return {
			"statusCode": 500,
			"body": json.dumps({"error": e.response["Error"]["Message"]}),
			"headers": {"Content-Type": "application/json"}
		}