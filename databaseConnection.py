import psycopg2
import os
PATH = os.path.dirname(__file__)



def build_database_connection_string():

    filename = os.path.join(PATH,'config.ini')
    try:
            with open(filename) as f:
                for line in f.readlines():
                    if 'host=' in line:
                        host = line.split('host=')[1].strip()
                        continue
                    elif 'dbname=' in line:
                        dbname = line.split('dbname=')[1].strip()
                    elif 'user' in line:
                        user = line.split('user=')[1].strip()
                    elif 'password=' in line:
                        password = line.split('password=')[1].strip()

    except:

            f = open(filename)
            for line in f.readlines():
                    if 'host=' in line:
                        host = line.split('host=')[1].strip()
                        continue
                    elif 'dbname=' in line:
                        dbname = line.split('dbname=')[1].strip()
                    elif 'user' in line:
                        user = line.split('user=')[1].strip()
                    elif 'password=' in line:
                        password = line.split('password=')[1].strip()
            f.close()

    connection_string = "host=%s dbname=%s user=%s password=%s" % (host,dbname,user,password)
    return connection_string

#########GET ROW FROM d_code TABLE BASE ON LAYER SPECIFIED ON column argument#########
def return_row_from_database(connection):

        cod_civ_list = []
        toponimo_list = []
        nome_via_list = []
        cfradesc_list = []
        civico_list = []
        barrato_list = []
        cod_via_ascot_list = []
        data_ascot_list = []
        gid_geom_list = []
        cod_via_str_list = []
        geom_list = []
        cursor = connection.cursor()
        #query = 'select cod_civ, toponimo, nome_via, cfradesc, civico, barrato, cod_via_ascot, data_ascot, gid_geom	,cod_via_str, ST_AsText(ST_Centroid(geom)) as geom  from test.v_civ_ascot_nongeo order by cod_civ'
        query = 'select cod_civ, toponimo, data_ascot, ST_AsText(ST_Centroid(geom)) as geom  from test.v_civ_ascot_nongeo order by cod_civ'

        cursor.execute(query)
        rows = cursor.fetchall()

        for r in rows:
            cod_civ_list.append(r[0])
            toponimo_list.append(r[1])
            #nome_via_list.append(r[2])
            #cfradesc_list.append(r[3])
            #civico_list.append(r[4])
            #barrato_list.append(r[5])
            #cod_via_ascot_list.append(r[6])
            data_ascot_list.append(r[2])
            #gid_geom_list.append(r[8])
            #cod_via_str_list.append(r[9])
            geom_list.append(r[3])
        tcolumn = ['cod_civ', 'toponimo', 'data_ascot']
        row_num = len(rows)
        col_num = len(tcolumn)
        #tcolumn = ['cod_civ', 'toponimo', 'nome_via', 'cfradesc', 'civico', 'barrato', 'cod_via_ascot', 'data_ascot', 'gid_geom','cod_via_str']

        trows = []
        #trows.extend([cod_civ_list,toponimo_list,nome_via_list, cfradesc_list, civico_list,barrato_list,cod_via_ascot_list,data_ascot_list,gid_geom_list, cod_via_str_list, geom_list])
        trows.extend([cod_civ_list,toponimo_list, data_ascot_list, geom_list])
        # data = {'cod_civ': cod_civ_list, 'toponimo':toponimo_list, 'nome_via':nome_via_list, 'cfradesc':cfradesc_list, 'civico':civico_list, 'barrato':barrato_list,
        #         'cod_via_ascot':cod_via_ascot_list, 'data_ascot':data_ascot_list, 'gid_geom':gid_geom_list	,'cod_via_str':cod_via_str_list}
        data = {'cod_civ': cod_civ_list, 'toponimo':toponimo_list, 'data_ascot':data_ascot_list}
        return tcolumn, trows, col_num, row_num



#######OPEN A POSTGRESQL CONNECTION AND MAKE THE QUERY#
#######MANAGE EVENTUALLY WITH ERROR EXCEPTION

def build_table_from_database_table():

    """

    :param schema: database schema
    :param table: name of table
    :return: a list of elements from databases grouped by categories. Each element is composed by:
             (category, [list of codes], [list od descriptions], [list of boolean is cheched], order -- not usefull)

    """
    CONNECTION_STRING = build_database_connection_string()
    try:
        with psycopg2.connect(CONNECTION_STRING) as connection:
            tcolumn, trows, col_num, row_num= return_row_from_database(connection)


    except:

        connection = psycopg2.connect(CONNECTION_STRING)
        tcolumn, trows, col_num, row_num = return_row_from_database(connection)
        connection.close()

    return tcolumn, trows, col_num, row_num


