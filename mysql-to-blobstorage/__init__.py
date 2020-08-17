import logging
import azure.functions as func
import mysql.connector


import pathlib
def get_ssl_cert():
    current_path = pathlib.Path(__file__).parent.parent
    return str(current_path / 'BaltimoreCyberTrustRoot.crt.pem')

def main(req: func.HttpRequest,outputblob: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    # Connect to MySQL
    cnx = mysql.connector.connect(
        user="suket@mysqltest-suket", 
        password='sCdGtHup2Fio8Rzs', 
        host="mysqltest-suket.mysql.database.azure.com", 
        port=3306,
        ssl_ca=get_ssl_cert()
    )
    logging.info(cnx)
    # Query table
    cursor = cnx.cursor()
    cursor.execute("select * from suket.tasks;")
    result_list = cursor.fetchall()
    # Build result response text
    result_str_list = []
    for row in result_list:
        row_str = ','.join([str(v) for v in row])
        result_str_list.append(row_str)
    result_str = '\n'.join(result_str_list)
    outputblob.set(result_str)

    logging.info(f"----- File write successful")

    return func.HttpResponse(
        "File Written to Blob Container ♥",
        status_code=200
    )