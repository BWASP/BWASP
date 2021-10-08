import csv
import sqlalchemy as db

print("csv -> db (create)")

# sqlalchemy -> sqlite3 db connect
db_engine = db.create_engine('sqlite:///databases/CVE.db')
db_connection = db_engine.connect()
db_metadata = db.MetaData()
db_table = db.Table('CVE', db_metadata, autoload=True, autoload_with=db_engine)
# print(table.columns.keys())

# db initialization
query = db.delete(db_table)
result = db_connection.execute(query)
print("DB initialization check")

# cve -> db insert
with open('./databases/cve_list.csv', 'r', encoding='ISO-8859-1') as f:
    csv_data = csv.reader(f)
    for row in csv_data:
        query = db.insert(db_table).values(year=row[0], description=row[2])
        result = db_connection.execute(query)
        result.close()

    print("Success")
