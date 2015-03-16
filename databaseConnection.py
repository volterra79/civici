import psycopg2

CONNECTION_STRING = "host='localhost' dbname='nepi_geo' user='postgres' password='postgres'"

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
        query = 'select cod_civ, toponimo, nome_via, cfradesc, civico, barrato, cod_via_ascot, data_ascot, gid_geom	,cod_via_str, geom  from test.v_civ_ascot_nongeo order by cod_civ '
        cursor.execute(query)
        rows = cursor.fetchall()
        row_num = len(rows)
        col_num = 10
        for r in rows:
            cod_civ_list.append(r[0])
            toponimo_list.append(r[1])
            nome_via_list.append(r[2])
            cfradesc_list.append(r[3])
            civico_list.append(r[4])
            barrato_list.append(r[5])
            cod_via_ascot_list.append(r[6])
            data_ascot_list.append(r[7])
            gid_geom_list.append(r[8])
            cod_via_str_list.append(r[9])

        tcolumn = ['cod_civ', 'toponimo', 'nome_via', 'cfradesc', 'civico', 'barrato', 'cod_via_ascot', 'data_ascot', 'gid_geom','cod_via_str']
        trows = []
        trows.extend([cod_civ_list,toponimo_list,nome_via_list, cfradesc_list, civico_list,barrato_list,cod_via_ascot_list,data_ascot_list,gid_geom_list, cod_via_str_list])
        data = {'cod_civ': cod_civ_list, 'toponimo':toponimo_list, 'nome_via':nome_via_list, 'cfradesc':cfradesc_list, 'civico':civico_list, 'barrato':barrato_list,
                'cod_via_ascot':cod_via_ascot_list, 'data_ascot':data_ascot_list, 'gid_geom':gid_geom_list	,'cod_via_str':cod_via_str_list}

        return tcolumn, trows, col_num, row_num


        #[(Decimal('7012'), 'VIA MUZIO CLEMENTI 7/B', 'VIA MUZIO CLEMENTI', None, Decimal('7'), 'B', Decimal('184'), datetime.date(2015, 1, 22), None, Decimal('184'))]
        #data = {'col1':['1','2','3'], 'col2':['4','5','6'], 'col3':['7','8','9']}


#######OPEN A POSTGRESQL CONNECTION AND MAKE THE QUERY#
#######MANAGE EVENTUALLY WITH ERROR EXCEPTION

def build_table_from_database_table():

    """

    :param schema: database schema
    :param table: name of table
    :return: a list of elements from databases grouped by categories. Each element is composed by:
             (category, [list of codes], [list od descriptions], [list of boolean is cheched], order -- not usefull)

    """
    try:
        with psycopg2.connect(CONNECTION_STRING) as connection:
            tcolumn, trows, col_num, row_num = return_row_from_database(connection)


    except:

        connection = psycopg2.connect(CONNECTION_STRING)
        tcolumn, trows, col_num, row_num = return_row_from_database(connection)
        connection.close()

    return tcolumn, trows, col_num, row_num


