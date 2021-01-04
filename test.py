import pymysql
import binascii

connection = pymysql.connect('Localhost', 'danro', 'sithlord', 'shoplite')
cursor = connection.cursor()

reporter_username = 'danroy'
reported_code = 'GRP34CS'
query_members = f"SELECT `email` , `number` FROM `register` WHERE `username`='shabadoo'"
cursor.execute(query_members)
connection.commit()
reported_results = cursor.fetchall()
for reported_result in reported_results:
    email_result = reported_result[0]
    number_result = reported_result[1]
query_report = f"INSERT INTO `reports`(`reporter`,`reported_username`,`reported_email`,`reported_number`,`reported_product`) VALUES ('{reporter_username}','shabadoo','{email_result}','{number_result}','{reported_code}')"
cursor.execute(query_report)
connection.commit()
