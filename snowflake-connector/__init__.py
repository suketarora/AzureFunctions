import logging

import azure.functions as func

import snowflake.connector
import os

def get_secret(conf_value) -> str:
     print(os.getenv(conf_value))
     return os.getenv(conf_value)

def parse_connection_secret(secret: str) -> dict:
    split_secret = secret.split(":")
    print(split_secret)
    # Warning("hi")
    return {
            "user": split_secret[0],
            "password": split_secret[1],
            "account": split_secret[2],
            "warehouse": split_secret[3],
            "database": split_secret[4],
            "schema": split_secret[5]
            
        }
        
def get_connection():
    # sec = parse_connection_secret(get_secret('SnowflakeCredendials'))
    sec = parse_connection_secret(os.getenv('SnowflakeCredendials'))
    print(sec)
    return snowflake.connector.connect(
        user=sec['user'],
        password=sec['password'],
        account=sec['account'],
        warehouse=sec['warehouse'],
        database=sec['database'],
        schema=sec['schema']
    )

    # return snowflake.connector.connect(
    #     user='SUKET',
    #     password='sCdGtHup2Fio8Rzs',
    #     account='xt25243.east-us-2.azure',
    #     warehouse='COMPUTE_WH'
    # )


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    print (os.getenv("SnowflakeCredendials"))
    ctx = get_connection()
    result_string = ""

    schema = req.params.get('schema')
    table = req.params.get('table')

    if schema and table and ctx :
        cursor = ctx.cursor()

        try:
            results = cursor.execute("SELECT * FROM SNOWFLAKE_SAMPLE_DATA.{}.{}".format(schema, table))
            for row in results:
                result_string = result_string + str(row[0]) + " " + str(row[1]) + "\n"
            result_string += "\n\nQuery ID: " + cursor.sfqid
        except Exception as e:
            print(e)
        finally:
            cursor.close()
        ctx.close()

        return func.HttpResponse(result_string)
    else:
        return func.HttpResponse(
             "Request failed.",
             status_code=400
        )