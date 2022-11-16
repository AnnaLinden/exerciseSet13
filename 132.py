# Implement a backend service that gets the ICAO code of an airport and then returns the name and location of the
# airport in JSON format. The information is fetched from the airport database used on this course. For example,
# the GET request for EFHK would be: http://127.0.0.1:5000/airport/EFHK. The response must be in the format of: {
# "ICAO":"EFHK", "Name":"Helsinki-Vantaa Airport", "Location":"Helsinki"}.

import json
from flask import Flask, Response, request
import mysql.connector

connection = mysql.connector.connect(
    host = "127.0.0.1",
    port = 3306,
    database = "flight_game",
    user = "test",
    password = "test",
    autocommit = True
)

app = Flask(__name__)
@app.route('/airport/<icao>')
def get_airport_and_city (icao):
    try:
        sql = "select airport.name, country.name from airport,country"
        sql += " where airport.iso_country = country.iso_country and airport.ident = '" + icao + "'";
        # print(sql)
        cursor = connection.cursor()
        cursor.execute(sql)
        response = cursor.fetchall()
        result = {"ICAO": icao, "Airport Name": response[0][0], "Location": response [0][1]}
        return result

    except ValueError:
        response = {
            "message": "Invalid ICAO code.",
            "status": 400
        }
        json_response = json.dumps(response)
        http_response = Response(response=json_response, status=400, mimetype="application/json")
        return http_response

@app.errorhandler(404)
def page_not_found(error_code):
    response = {
        "message": "Invalid endpoint",
        "status": 404
    }
    json_response = json.dumps(response)
    http_response = Response(response=json_response, status=404, mimetype="application/json")
    return http_response


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=5000)