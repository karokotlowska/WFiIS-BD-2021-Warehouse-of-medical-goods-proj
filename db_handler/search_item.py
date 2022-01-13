from magazyn_proj import settings
import psycopg2


def create_data_from_fetch(mobile_records,cursor):
    column_names = [column[0] for column in cursor.description]
    cursor.execute("SELECT id_zamowienia, status FROM magazyn.zamowienie;")
    data = [{} for _ in range(len(mobile_records))]
    for i in range(len(mobile_records)):
        for j in range(len(mobile_records[i])):
            data[i][column_names[j]] = mobile_records[i][j]
   
    return data


def filter(data):
    cleanedData  = {a:b for a,b in data.items()}
    checkBoxStatus = []
    sort=[]
    kwota=[]
    
    
    for desc,value in cleanedData.items():
        if value == 'on':
            if desc == 'aktywne' or desc == 'w realizacji' or desc == 'zrealizowane':
               checkBoxStatus.append(desc)
               print()
        if 'sort' == desc:
            sort.append(value)
        if 'kwota' in desc:
            kwota.append(value)
        
    statusQuery = ""
    if len(checkBoxStatus) > 0:
        statusQuery+= checkBoxStatus[0]
        if len(checkBoxStatus) > 1:
            for x in checkBoxStatus[1:]:
                statusQuery+="|"+x
    
  

    con = psycopg2.connect(database=settings.DATABASE['NAME'], user=settings.DATABASE['USER'], password=settings.DATABASE['PASSWORD'], host=settings.DATABASE['HOST'], port=settings.DATABASE['PORT'])
    cur = con.cursor()
    if len(sort) >0 :
        sort.append(cleanedData["sort_type"])
        postgreSQL_select_Query = '''SELECT z.numer_kolejny_zamowienia, z.id_zamowienia, z.data_stworzenia, z.status, z.kwota FROM magazyn.zamowienie Z
                                    
                                    
                                    
                                    AND (kwota BETWEEN {} AND {})
                                    WHERE z.status ~* \'{}\'
                                    ORDER BY {} {}
                                    '''.format(statusQuery,kwota[0],kwota[1],sort[0],sort[1])
        cur.execute(postgreSQL_select_Query)
        mobile_records = cur.fetchall()
    else:
        postgreSQL_select_Query = '''SELECT z.numer_kolejny_zamowienia, z.id_zamowienia, z.data_stworzenia, z.status, z.kwota FROM magazyn.zamowienie Z
                                    
                                    
                                    WHERE z.status ~* \'{}\'
                                   
                                   
                                    '''.format(statusQuery)
        cur.execute(postgreSQL_select_Query)
        mobile_records = cur.fetchall()

    if mobile_records is None:
        cur.close()
        con.close()
        return []
    else:
        return_data = create_data_from_fetch(mobile_records,cur)
      
    return return_data