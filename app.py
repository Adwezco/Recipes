from flask import Flask, json, render_template, request
from flaskext.mysql import MySQL
app = Flask(__name__)

mysql = MySQL()


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'recipes'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/api/getadd")
def getadd():
    return render_template('add.html')

@app.route("/api/add", methods=['POST'])
def add():
    try:
        _ingredientName = request.form['ingredientname']
        _ingredientQuantity = request.form['quantity']
        _dishName = request.form['dishname']
        _dishDescription = request.form['dishdescription']

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.callproc('sp_add2', (_ingredientName, _ingredientQuantity, _dishName, _dishDescription))
        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'message': 'User created successfully !'})
        else:
            return json.dumps({'error': str(data[0])})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run()