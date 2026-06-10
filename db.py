import boto3
import os
import uuid
from dotenv import load_dotenv
from boto3.dynamodb.conditions import Attr

load_dotenv()

def get_table():
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.getenv('AWS_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN')
    )
    return dynamodb.Table(os.getenv('TABLE_NAME'))

def add_product(name, description, category, price, stock, image_url):
    table = get_table()
    product_id = str(uuid.uuid4())
    table.put_item(Item={
        'PK': f'PRODUCT#{product_id}',
        'SK': 'METADATA',
        'product_id': product_id,
        'name': name,
        'description': description,
        'category': category,
        'price': price,
        'stock': int(stock),
        'image_url': image_url
    })
    return product_id

def get_all_products():
    table = get_table()
    response = table.scan(
        FilterExpression=Attr('SK').eq('METADATA')
    )
    return response['Items']

def get_product(product_id):
    table = get_table()
    response = table.get_item(Key={
        'PK': f'PRODUCT#{product_id}',
        'SK': 'METADATA'
    })
    return response.get('Item')

def update_product(product_id, name, description, category, price, stock, image_url):
    table = get_table()
    table.update_item(
        Key={'PK': f'PRODUCT#{product_id}', 'SK': 'METADATA'},
        UpdateExpression='SET #n = :n, description = :d, category = :c, price = :p, stock = :s, image_url = :i',
        ExpressionAttributeNames={'#n': 'name'},
        ExpressionAttributeValues={
            ':n': name,
            ':d': description,
            ':c': category,
            ':p': price,
            ':s': int(stock),
            ':i': image_url
        }
    )

def delete_product(product_id):
    table = get_table()
    table.delete_item(Key={
        'PK': f'PRODUCT#{product_id}',
        'SK': 'METADATA'
    })