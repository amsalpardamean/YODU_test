from flask import Flask,jsonify,request
import psycopg2
import json
app = Flask(__name__)

conn = psycopg2.connect(
   database="event", user='postgres', password='12345', host='localhost', port= '5432'
)

jsonHeader =  {"teams": []}
jsonTeam = {
    "team_id": 0,
    "team_name": ""
  }

jsonRes =  {"data": []}

resTemplete = {
  "tourney_id": "",
  "name": "",
  "games": {
    "game_id": "",
    "game_name": ""
  },
  "status": ""
}


def teamLookUp(id):
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("select id, name from game.tabel_team tt "
    "where id = 1 "
    )
    result = cursor.fetchall();

    for i in result:
        jsonTeam["team_id"] = i[0]
        jsonTeam["team_name"] = i[1]

        jsonHeader['teams'].append(jsonTeam)
    return jsonHeader


def tournamenLookUp():
    conn.autocommit = True
    cursor = conn.cursor()

    sql = ("select t1.id, t1.name,t4.id, t4.name, t1.status, t2.id, t2.name "
    " from game.tabel_team_to_tournament t3 "
    " join game.tabel_tournament t1 on t1.id = t3.id_tournament "
    " join game.tabel_team t2 on t2.id = t3.id_team "
    " join game.tabel_games t4 on t4.id = t1.id_games "
    " join game.tabel_user tu on tu.id = t2.created_by "
    " where t1.status = 'regis_open' and t2.status = 'active' "
    )

    cursor.execute(sql)

    result = cursor.fetchall();

    for i in result:
        jsonTour = resTemplete
        jsonTour['tourney_id'] = i[0]
        jsonTour['name'] = i[1]
        jsonTour['games']['game_id'] = i[2]
        jsonTour['games']['game_name'] = i[3]
        jsonTour['status'] = i[4]

        team = teamLookUp(i[5])
        jsonTour.update(team)
        jsonRes['data'].append(jsonTour)
    return jsonRes

@app.route('/post_json', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        req = request.get_json()
        id = req['userId']

        res = tournamenLookUp()

        @app.route('/recomended_tournament/1', methods = ['GET'])
        def example():
           return jsonify(jsonRes)

        if __name__ == '__main__':
            app.run(debug=True)

        return res
    else:
        return 'Content-Type not correct!'

@app.route('/')
def hello():
    return 'Selamat datang di dasboard YUDO!'

if __name__ == "__main__":
    app.run()
