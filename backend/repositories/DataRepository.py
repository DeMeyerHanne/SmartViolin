from .Database import Database

class projectDataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    # OM GRAFIEKEN TE MAKEN
    @staticmethod
    def read_alle_waarden(id):
        sql = 'SELECT eindDatum, gemetenWaarde FROM tblMeting WHERE deviceId = %s ORDER BY startDatum DESC LIMIT 7'
        params = [id]
        return Database.get_rows(sql, params)
    

    # temperatuur opvragen (1 rij)
    @staticmethod
    def read_alle_waarden_met_1():
        sql = 'SELECT gemetenWaarde FROM tblMeting WHERE deviceId = 1 ORDER BY startDatum DESC'
        return Database.get_one_row(sql)

    # luchtvochtigheid opvragen (1 rij)
    @staticmethod
    def read_alle_waarden_met_2():
        sql = 'SELECT gemetenWaarde FROM tblMeting WHERE deviceId = 2 ORDER BY startDatum DESC'
        return Database.get_one_row(sql)

    # oefentijd opvragen (1 rij)
    @staticmethod
    def read_alle_waarden_met_3():
        sql = 'SELECT oefentijd FROM vioolkofferdb.tblMeting WHERE deviceId = 3 ORDER BY startDatum DESC'
        return Database.get_one_row(sql)

    @staticmethod
    def insert_data_temp(codeS, deviceId, gemetenWaarde):
        sql = 'INSERT INTO vioolkofferdb.tblMeting (codeS, deviceId, startDatum, eindDatum, gemetenWaarde) VALUES (%s, %s, now(), now(), %s)'
        params = [codeS, deviceId, gemetenWaarde]
        return Database.execute_sql(sql, params)

    @staticmethod
    def insert_data_lucht(codeS, deviceId, gemetenWaarde):
        sql = 'INSERT INTO vioolkofferdb.tblMeting (codeS, deviceId, startDatum, eindDatum, gemetenWaarde) VALUES (%s, %s, now(), now(), %s)'
        params = [codeS, deviceId, gemetenWaarde]
        return Database.execute_sql(sql, params)

    @staticmethod
    def insert_data_oef(codeS, deviceId, gemetenWaarde, oefentijd):
        sql = 'INSERT INTO vioolkofferdb.tblMeting (codeS, deviceId, startDatum, eindDatum, gemetenWaarde, oefentijd) VALUES (%s, %s, now(), now(), %s, %s)'
        params = [codeS, deviceId, gemetenWaarde, oefentijd]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_status_koffer():
        sql = "SELECT * FROM tblMeting"
        return Database.get_one_row(sql)

    @staticmethod
    def update_status_koffer(id, status):
        sql = "SELECT codeS, gemetenWaarde FROM tblMeting WHERE codeS = 4"
        params = [id, status]
        return Database.execute_sql(sql, params)