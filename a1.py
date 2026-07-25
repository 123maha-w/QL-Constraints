import sqlite3
import pandas as pd

conn = sqlite3.connect('citie.db')

conn.execute("DROP TABLE IF EXISTS City;")

conn.execute("""
CERAT TABLE City (
    City_ID   INTEGER   PRIMARY KEY ,
    City_name   TEXT    NOT_NULL UNIQUE
    country    TEXT      NOT_NULL,
    POPULATION INTEGER ,
    IS_CAPITAL  TEXT    DEFAULT NO,
 );""")

conn.commit()
print("table created successfully")


conn.execute("INSERT INTO City VALUES(1, 'tokyo', 'japan', 13960000, 'yes');")

conn.execute("INSERT INTO City VALUES (2, 'Nairobi', 'Kenya', 4397000, 'Yes');")

conn.execute("INSERT INTO City VALUES (3, 'Mumbai', 'India', 20667656, 'No');")

conn.execute("INSERT INTO City VALUES (4, 'Sao Paulo', 'Brazil', 12325232, 'No');")

conn.execute("INSERT INTO City VALUES (5, 'London', 'UK', 9541000, 'Yes');")

conn.execute("INSERT INTO City (City_Id, City_Name, Country) VALUES (6, 'Sydney', 'Australia');")

conn.commit()
print("rows created successfully")
cities = pd.read_sql("SELECT * FROM City;"conn)
print(cities)

print("\n---testing PRIMARY KEY---")
try:
    conn.execute("INSERT INTO City VALUES(1, 'cairo', 'egypt', 21323000, 'yes');")
    conn.commit()

except Exception as e:
     conn.rollback()
     print("Rejected:", e)
     print("Country is NOT NULL — every row must provide a country value.")
print("\n--- Testing UNIQUE ---")

try:
    conn.execute("INSERT INTO City VALUES (8, 'Tokyo', 'Japan', 99999, 'No');")
    conn.commit()

except Exception as e:

    conn.rollback()
    print("Rejected:", e)
    print("City_Name is UNIQUE — 'Tokyo' is already in the table.")


print("\n--- DEFAULT value check for Sydney ---")
sydney = pd.read_sql("""SELECT City_Name, Country, Is_Capital
FROM City
WHERE City_Name == 'Sydney';""", conn)
print(sydney)
print("Is_Capital was not given — DEFAULT 'No' was used automatically.")


print("\n--- NULL in the Population column ---")
all_cities = pd.read_sql("""SELECT City_Name, Country, Population
FROM City;""", conn)

print(all_cities)    


missing = pd.read_sql("""SELECT City_Name FROM City WHERE Population IS NULL;""", conn)
print("Cities with no population data:")

print(missing)
has_data = pd.read_sql("""SELECT City_Name, Population FROM City WHERE Population IS NOT NULL;""", conn)
print("Cities with population data:")
print(has_data)

conn.close()