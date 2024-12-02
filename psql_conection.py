import psycopg2
import csv

db_config = {
    'dbname': 'proyecto2y3',
    'user': 'postgres',
    'password': 'nueva_contraseña',
    'host': 'localhost',
    'port': 5432
}

connection = psycopg2.connect(**db_config)
cursor = connection.cursor()


def init():
    with open(r"C:\Users\Camila\Desktop\styles\styles.csv", 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        cTableCommand = "CREATE TABLE IF NOT EXISTS styles (id INT, gender VARCHAR(10), masterCategory VARCHAR(25), subCategory VARCHAR(25), articleType VARCHAR(25), baseColour VARCHAR(25), season VARCHAR(10), year INT NULL, usage VARCHAR(25), productDisplayName VARCHAR(255))"
        cursor.execute(cTableCommand)

        # Iteración en cada fila
        for row in csv_reader:
            print(row)
            while len(row) > 10:
                print("Sz: ", len(row))
                print("Caso especial: ", row[len(row)-1])
                row[len(row) - 2] += row[len(row) - 1]
                row.pop()
                print("Nuevo display name: ", row[len(row)-2])
                print("Sz: ", len(row))
            id, gender, masterCategory, subCategory, articleType, baseColour, season, stryear, usage, productDisplayName = row
            if stryear == '':
                year = None
            else:
                year = int(stryear)


            cursor.execute("SELECT 1 FROM styles LIMIT 1")
            if cursor.fetchone() is None:
                cursor.execute(
                    "INSERT INTO styles (id, gender, masterCategory, subCategory, articleType, baseColour, season, year, usage, productDisplayName) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (id, gender, masterCategory, subCategory, articleType, baseColour, season, year, usage,
                     productDisplayName))

        connection.commit()
    cursor.execute("ALTER TABLE styles ADD COLUMN weighted_tsv tsvector")
    cursor.execute("ALTER TABLE styles ADD COLUMN weighted_tsv2 tsvector")
    cursor.execute(
        "UPDATE styles SET weighted_tsv = x.weighted_tsv, weighted_tsv2 = x.weighted_tsv FROM (SELECT id, setweight(to_tsvector('english', COALESCE(masterCategory,'')), 'A') || setweight(to_tsvector('english', COALESCE(articleType,'')), 'A') || setweight(to_tsvector('english', COALESCE(baseColour,'')), 'A') || setweight(to_tsvector('english', COALESCE(season,'')), 'A') || setweight(to_tsvector('english', COALESCE(usage,'')), 'A') || setweight(to_tsvector('english', COALESCE(productdisplayname,'')), 'B') AS weighted_tsv FROM styles) AS x WHERE x.id = styles.id;")
    cursor.execute("CREATE INDEX weighted_tsv_idx ON styles USING GIN (weighted_tsv2)")


def topKpsql(query, k):
    words = query.split(" ")
    terms = ""
    for word in words:
        terms += word + " | "
    terms = terms[:-2]

    print("Terminos leidos: ", terms)

    cursor.execute("set enable_seqscan = false")
    #print("hola")
    consulta = f"SELECT id, gender, mastercategory, subcategory, articletype, basecolour, season, year, usage, productdisplayname FROM styles, to_tsquery('english', '{terms}') query WHERE query @@ weighted_tsv2 ORDER BY ts_rank_cd(weighted_tsv2, query) desc LIMIT {k};"
    #print("hola")
    cursor.execute(consulta)
    #print("hola")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


init()
query = "adidas shoes red"
k = 5

topKpsql(query, k)

cursor.close()
connection.close()