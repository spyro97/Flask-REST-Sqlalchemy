import pyodbc

def read(conn):
    print("Lectura")
    cursor = conn.cursor()
    cursor.execute("select * from cat_areas")
    for row in cursor:
        print(row)
    print()

def create(conn):
    print("Insertar")
    cursor = conn.cursor()
    cursor.execute(
        'insert into cat_areas(nombre,clave_contable,fecha_registro,usuario_registro) values (?,?,?,?);',
        ('RECURSOS',5532,'2019-11-12',17)
    )    
    conn.commit()
    read(conn)

def update(conn):
    print("Actualizar")
    cursor= conn.cursor()
    cursor.execute(
        'update cat_areas set nombre=? where id_area=?;',
        ('dsfdfsfd',9)
    )
    conn.commit()
    read(conn)

def delete(conn):
    print("Eliminar")
    cursor= conn.cursor()
    cursor.execute('delete from cat_areas where id_area=14;')
    conn.commit()
    read(conn)


conn = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=172.16.1.108;"
    "Database=dsd_mazatlan;"
    "UID=sa;"
    "PWD=Dsdsistemas2012"
    
)


#read(conn)
#create(conn)
#update(conn)
delete(conn)

conn.close()