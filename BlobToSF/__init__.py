import logging
import snowflake.connector
import azure.functions as func

def get_connection():
    return snowflake.connector.connect(
        user='SUKET',
        password='sCdGtHup2Fio8Rzs',
        account='xt25243.east-us-2.azure',
        warehouse='COMPUTE_WH'
    )

def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    
    ctx = get_connection()
    result_string = ""
    if  ctx :
        cursor = ctx.cursor()
        try:
            cursor.execute("use MY_DB;")
            sql = '''copy into "MY_DB"."PUBLIC"."TASKS" from @BLOBSTORAGESTAGE FILE_FORMAT=(TYPE=csv skip_header=0);'''
            cursor.execute(sql)
            results = cursor.execute("""select * from "MY_DB"."PUBLIC"."TASKS" """)
            for row in results:
                result_string = result_string + str(row[0]) + "\n"
            result_string += "\n\nQuery ID: " + cursor.sfqid
            
        except Exception as e:
            print(e)
        finally:
            cursor.close()
        ctx.close()
        logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
        logging.info(result_string)