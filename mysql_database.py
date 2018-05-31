# Third-party
import mysql.connector, json
from mysql.connector import errorcode, connection
from datetime import datetime, date, time, timedelta


#0.1

def connect():
    try:
        cnx = connection.MySQLConnection(user='root', password='admin',
                                         host='127.0.0.1',
                                         database='carcounter')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        return cnx


# Le todos os sensores (mistirei portugues com ingles)
def read_sensores():
    # Connect to database
    cnx = connect()

    # Creates a cursor (object used to read from gotten streams)
    cursor = cnx.cursor()

    # String da query
    query = ("SELECT * FROM sensores")

    cursor.execute(query)
    print(cursor)

    # Dict pra retornar um JSON no webserver
    sensores_list = []

    for (idsensores, idusuario, lat, lon, nome, descricao) in cursor:
        sensores_list.append({'idsensor': idsensores, 'idusuario': idusuario, 'lat': lat, 'lon': lon, 'nome': nome,
                         'descricao': descricao})

    cursor.close()
    cnx.close()

    sensores = {'sensores':sensores_list}

    return sensores

def read_usuarios():
    # Connect to database
    cnx = connect()

    # Creates a cursor (object used to read from gotten streams)
    cursor = cnx.cursor()

    # String da query
    query = ("SELECT * FROM usuarios")

    cursor.execute(query)
    print(cursor)

    # Dict pra retornar um JSON no webserver
    usuarios_list = []

    for (idusuarios, nome, status, login, senha, email) in cursor:
        usuarios_list.append({'idusuario': idusuarios, 'nome': nome, 'status': status, 'login': login, 'senha': senha,
                         'email': email})

    cursor.close()
    cnx.close()

    usuarios = {'usuarios':usuarios_list}

    return usuarios


def logincheck(login, senha):
    # Connect to database
    cnx = connect()

    # Creates a cursor (object used to read from gotten streams)
    cursor = cnx.cursor()

    # String da query
    query = ("SELECT * FROM usuarios where login = %s and senha = %s")


    cursor.execute(query, (login, senha))
    user=cursor.fetchone()

    return user



def read_carros():
    # Connect to database
    cnx = connect()

    # Creates a cursor (object used to read from gotten streams)
    cursor = cnx.cursor()

    # String da query
    query = ("SELECT * FROM carros")

    cursor.execute(query)


    # Dict pra retornar um JSON no webserver
    carros_list = []

    for (idcarros, horario, idsensor) in cursor:
        carros_list.append({'idcarros': idcarros, 'idsensor':idsensor , 'horario': horario})

    cursor.close()
    cnx.close()

    carros = {'carros':carros_list}

    return carros

def read_carrostabela(dia, idsensor):
    # Connect to database
    cnx = connect()

    # Creates a cursor (object used to read from gotten streams)
    cursor = cnx.cursor()

    # String da query
    query = ("SELECT * FROM carros WHERE horario between '"+dia +" 00:00:00' and '" + dia + " 23:59:59' and idsensor =" + idsensor)

    cursor.execute(query)


    # Dict pra retornar um JSON no webserver
    carros_list = []

    for (idcarros, horario, idsensor) in cursor:
        carros_list.append({'idcarros': idcarros, 'idsensor':idsensor , 'horario': horario})

    cursor.close()
    cnx.close()

    carros = {'carros':carros_list}

    return carros



def read_carrosdia(dia, id):
    # Connect to database
    cnx = connect()

    # Creates a cursor (object used to read from gotten streams)
    cursor = cnx.cursor(buffered=True)
    # String da query

    t = time(00, 00)
    t = time(t.hour + 1, 00)
    contagem = {}
    for i in range(24):
        t = time(00, 00)
        t = time(t.hour + i, 00)
        querystring = ("select count(idcarros) from carros where horario between '" + dia + " " + str(
            t.hour) + ":00:00' and '" + dia + " " + str(t.hour) + ":59:59' and idsensor="+id)
        query = (querystring)
        cursor.execute(query)
        var = cursor.fetchall()
        var1 = var[0][0]
        dictstr = str(i)
        contagem[dictstr] = var1
    print(contagem)
    # Dict pra retornar um JSON no webserver
    cursor.close()
    cnx.close()

    return contagem

def read_carroscalendario(diai, diaf, id):

    cnx = connect()
    cursor = cnx.cursor(buffered=True)

    a = datetime.strptime(diai, "%Y-%m-%d")
    b = datetime.strptime(diaf, "%Y-%m-%d")
    delta=b-a

    dias_list = []
    dia=datetime.strptime(diai, "%Y-%m-%d")
    for i in range(delta.days):
        diaq=str(dia.year)+"-"+str(dia.month)+"-"+str(dia.day)
        dia+= timedelta(days=1)
        querystring = ("select count(idcarros) from carros where horario between '" + diaq + " 00:00:00' and '" + diaq + " 23:59:59' and idsensor=" + str(id))
        query = (querystring)
        cursor.execute(query)
        var = cursor.fetchall()
        dias_list.append(var[0][0])
    dias = {'carros': dias_list}

    return dias



    #
    #
    #
    #
    #
    #

    #print(contagem)
    # Dict pra retornar um JSON no webserver
    #cursor.close()
    #cnx.close()

    return







def insert_carro(carro):
    """
    Funcao para inserir um sensor no banco. Lucas viado essa porra aceita dict tbm dict mesma merda que JSON quase

    :param sensor: dict contendo os dados de um sensor
    :type sensor: dict
    :return:
    """

    cnx = connect()

    cursor = cnx.cursor()
    query = ("INSERT INTO carros (horario, idsensor) "
             "VALUES (%(horario)s,%(idsensor)s)")

    # Insert new employee
    cursor.execute(query, carro)
    idcarro = cursor.lastrowid

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()
    return idcarro

def insert_sensores(sensor):
    """
    Funcao para inserir um sensor no banco. Lucas viado essa porra aceita dict tbm dict mesma merda que JSON quase

    :param sensor: dict contendo os dados de um sensor
    :type sensor: dict
    :return:
    """

    cnx = connect()

    cursor = cnx.cursor()

    query = ("INSERT INTO sensores (idusuario, lat, lon, nome, descricao) "
             "VALUES (%(idusuario)s, %(lat)s, %(lon)s, %(nome)s, %(descricao)s)")

    # Insert new employee
    print(sensor)
    cursor.execute(query, sensor)
    idsensor = cursor.lastrowid

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()
    return idsensor

def updatesensor(sensor):
    """
    Funcao para inserir um sensor no banco. Lucas viado essa porra aceita dict tbm dict mesma merda que JSON quase

    :param sensor: dict contendo os dados de um sensor
    :type sensor: dict
    :return:
    """

    cnx = connect()
    print(sensor["lat"])
    cursor = cnx.cursor()

    query = ("UPDATE sensores SET idusuario =%(idusuario)s"
             ", lat=%(lat)s, lon=%(lon)s, nome=%(nome)s, descricao=%(descricao)s WHERE idsensores=%(idsensor)s")

    # Insert new employee
    print(sensor)
    cursor.execute(query, sensor)
    idsensor = cursor.lastrowid

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()
    return idsensor

def insert_usuario(usuario):
    """
    Funcao para inserir um sensor no banco. Lucas viado essa porra aceita dict tbm dict mesma merda que JSON quase

    :param sensor: dict contendo os dados de um sensor
    :type sensor: dict
    :return:
    """

    cnx = connect()

    cursor = cnx.cursor()

    query = ("INSERT INTO usuarios (idusuarios, nome, status, login, senha, email) "
             "VALUES (%(idusuarios)s, %(nome)s, %(status)s, %(login)s, %(senha)s, %(email)s)")

    # Insert new employee
    print(usuario)
    cursor.execute(query, usuario)
    idusuario = cursor.lastrowid

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()
    return idusuario
