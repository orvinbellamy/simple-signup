import json
import logging
import boto3
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
	
	table_name = 'AppData'
	table = dynamodb.Table(table_name)

	# Since this is just a demo, the number of sessions is limited to 100
	# If number of items in the DynamoDB table is equal to 100, return an error
	try:
		scan_resp = table.scan(Select='COUNT')
		item_count = scan_resp.get('Count', 0)
		if item_count >= 100:
			return {
				'statusCode': 400,
				'body': json.dumps({'error': 'Maximum number of sessions reached.'})
			}
	except Exception as e:
		logger.error(f"Error counting items: {e}")
		return {
			'statusCode': 500,
			'body': json.dumps({'error': 'Could not count items in the table.'})
		}

	try:
		new_session = json.loads(event['body'])
		
	except Exception as e:
		logger.error(f"Malformed JSON: {e}")
		return {
			'statusCode': 400,
			'body': json.dumps({'error': 'Malformed JSON in request body.'})
		}

	logger.info(f'EVENT BODY: {json.dumps(new_session, default=str)}')

	try:
		response = table.put_item(Item=new_session)

		logger.info(f"Session is successfully created: PK={new_session['PK']}, SK={new_session['SK']}")

		return {
			'statusCode': 200,
			'body': json.dumps({
				'message': 'Registrations updated',
				'session': response.get('Attributes', {})
			})
		}
	except Exception as e:
		print("Update error:", e)
		return {
			'statusCode': 500,
			'body': json.dumps({ 'error': 'Could not create session.' })
		}