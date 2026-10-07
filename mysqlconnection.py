import pymysql.cursors
class MySQLConnection:
    def __init__(self,db):
        connection= pymysql.connect(
            host='localhost', #servidor local
            user='root', #usuario de la bd
            password='1234', #password de la base datos
            database=db, #nombre de la bd
            charset='utf8mb4', #conjunto de caracteres BD
            cursorclass=pymysql.cursors.DictCursor, #define un curso de tipo de diccionario
            #cursor: es una clase que permite manipular las filas de una tabla
            autocommit=True #confirmar las operaciones automaticamente

        )
        self.connection=connection
        #ejecuta la consulta SQL en MySQL
    def query_db(self,query,data=None):
        #un paquete que permite manipular filas de una tabla
        with self.connection.cursor() as cursor:
            try:
                query=cursor.mogrify(query,data)
                print("Corriendo la consulta",query)
                executable= cursor.execute(query,data)
                if query.lower().find("insert")>=0:
                    self.connection.commit()#confirmar la insersion de un registro
                    return cursor.lastrowid #retorna el ultimo id de la tabla
                elif query.lower().find("select")>=0:
                    result = cursor.fetchall()#recuperar todas las filas de un select
                    return result
                else:
                    self.connection.commit()
            except Exception as e:
                print("Error",e) #imprimir error por defecto
                return False
            finally:
                self.connection.close()

def connectMySQL(db):
    return MySQLConnection(db) #returna un objeto MYSQLConnection
