import json
import logging
import boto3
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):

	updates = json.loads(event['body'])
	logger.info(f'EVENT BODY: {json.dumps(updates, default=str)}')
	
	table_name = 'AppData'
	table = dynamodb.Table(table_name)
	
	update_data = json.loads(event['body'])

	pk = update_data['PK'] # partition key
	sk = update_data['SK'] # sort key
	registration = update_data['registration']
	waitlist = update_data['waitlist']

	try:
		response = table.update_item(
			Key={
				'PK': pk,
				'SK': sk
			},
			UpdateExpression='SET registration = :r, waitlist = :w',
			ExpressionAttributeValues={
				':r': registration,
				':w': waitlist
			},
			ReturnValues='UPDATED_NEW'
		)

		logger.info(f"StatusCode: 200, session is successfully updated: {response.get('Attributes', {})}")

		return {
			'statusCode': 200,
			'headers': {
				'Cache-Control': 'no-store',
				'Pragma': 'no-cache'
			},
			'body': json.dumps({
				'message': 'Registrations updated',
				'session': response.get('Attributes', {})
			})
		}
	except Exception as e:
		print("Update error:", e)
		return {
			'statusCode': 500,
			'body': json.dumps({ 'error': 'Could not update session.' })
		}