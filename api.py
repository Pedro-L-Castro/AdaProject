from flask import Flask, jsonify
import pyodbc

app = Flask(__name__)

# Configuração do banco de dados SQL Server
db_config = {
    'driver': 'ODBC Driver 18 for SQL Server',  # Substitua se estiver usando outro driver
    'server': 'adaproject-server.database.windows.net',  # Nome ou IP do servidor
    'database': 'ada-db',  # Nome do banco
    'username': 'pedro',  # Usuário do banco
    'password': 'Pl123456'  # Senha do banco
}

# Função para conectar ao banco de dados
def get_db_connection():
    connection_string = (
        f"DRIVER={db_config['driver']};"
        f"SERVER={db_config['server']};"
        f"DATABASE={db_config['database']};"
        f"UID={db_config['username']};"
        f"PWD={db_config['password']}"
    )
    return pyodbc.connect(connection_string)

@app.route('/times', methods=['GET'])
def get_all_times():
    try:
        # Conectar ao banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()

        # Executar consulta SQL
        cursor.execute("SELECT id, nome FROM times")
        rows = cursor.fetchall()

        # Transformar os resultados em uma lista de dicionários
        times = [{'id': row.id, 'nome': row.nome} for row in rows]

        # Fechar conexão
        cursor.close()
        conn.close()

        # Retornar resultados como JSON
        return jsonify(times), 200
    except pyodbc.Error as err:
        return jsonify({'error': str(err)}), 500
    

@app.route('/times/<int:id>', methods=['GET'])
def get_time_by_id(id):
    try:
        # Conectar ao banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()

        # Executar consulta SQL
        cursor.execute(f"SELECT id, nome FROM times WHERE id = {id}")
        rows = cursor.fetchall()

        # Transformar os resultados em uma lista de dicionários
        time = [{'id': row.id, 'nome': row.nome} for row in rows]

        # Fechar conexão
        cursor.close()
        conn.close()

        # Retornar resultados como JSON
        return jsonify(time), 200
    except pyodbc.Error as err:
        return jsonify({'error': str(err)}), 500
    



if __name__ == '__main__':
    app.run(debug=True)
