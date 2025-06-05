import json
import logging
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

	logger.info("FULL EVENT: " + json.dumps(event, default=str))
	
	body = json.loads(event['body'])
	username = body.get('username')

	if username == '' or username is None:
		return {
			"statusCode": 400,
			"body": json.dumps({"error": "Username is required"})
		}

	dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
	table = dynamodb.Table("AppData")

	try:
		# This doesn't work because session_id is not the PK, so we need to use GSI
		# resp = TABLE.get_item(Key={"session_id": session_id})

		resp = table.get_item(
			Key={
				'PK': username,
				'SK': 'ACCOUNT'
			}
		)

		item = resp['Item']

		# If item exists
		if item :
			session_data = item
			return {
				"statusCode": 200,
				'headers': {
					'Cache-Control': 'no-store',
					'Pragma': 'no-cache'
				},
				"body": json.dumps(session_data, default=str),
				"headers": {"Content-Type": "application/json"}
			}
			
		# If item does not exist
		else:	
			return {
				"statusCode": 404,
				"body": json.dumps({"message": "Username not found"})
			}
		
	except ClientError as e:
		return {
			"statusCode": 500,
			"body": json.dumps({"error": e.response["Error"]["Message"]})
		}