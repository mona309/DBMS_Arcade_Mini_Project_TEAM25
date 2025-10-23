from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)

# Database configuration - Direct values (Update with your MySQL password)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',  # CHANGE THIS to your MySQL root password
    'database': 'arcade',
    'port': 3306
}

def get_db_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def execute_query(query, params=None, fetch=True):
    """Execute database query with error handling"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
        else:
            connection.commit()
            result = {"affected_rows": cursor.rowcount, "lastrowid": cursor.lastrowid}
        
        cursor.close()
        connection.close()
        return result
    except Error as e:
        print(f"Query execution error: {e}")
        if connection:
            connection.close()
        return None

# =====================================================
# ROUTES
# =====================================================

@app.route('/')
def index():
    """Homepage with statistics"""
    stats = {
        'total_players': 0,
        'total_games': 0,
        'active_sessions': 0,
        'total_achievements': 0
    }
    
    # Get statistics
    result = execute_query("SELECT COUNT(*) as count FROM player")
    if result:
        stats['total_players'] = result[0]['count']
    
    result = execute_query("SELECT COUNT(*) as count FROM game")
    if result:
        stats['total_games'] = result[0]['count']
    
    result = execute_query("SELECT COUNT(*) as count FROM multiplayersession WHERE EndTime IS NULL")
    if result:
        stats['active_sessions'] = result[0]['count']
    
    result = execute_query("SELECT COUNT(*) as count FROM achievement")
    if result:
        stats['total_achievements'] = result[0]['count']
    
    return render_template('index.html', stats=stats)

@app.route('/players')
def players():
    """Display all players"""
    query = """
        SELECT p.PlayerID, p.Username, p.Email, p.TotalScore, 
               p.Avatar, r.RankName, p.RegistrationDate
        FROM player p
        LEFT JOIN ranks r ON p.RankID = r.RankID
        ORDER BY p.TotalScore DESC
    """
    players_list = execute_query(query)
    return render_template('players.html', players=players_list or [])

@app.route('/player/<int:player_id>')
def player_detail(player_id):
    """Player profile page"""
    # Get player info
    query = "SELECT p.*, r.RankName FROM player p LEFT JOIN ranks r ON p.RankID = r.RankID WHERE p.PlayerID = %s"
    player = execute_query(query, (player_id,))
    
    if not player:
        return "Player not found", 404
    
    player = player[0]
    
    # Get achievements
    query = """
        SELECT a.Name, a.Description, pa.DateEarned
        FROM playerachievement pa
        JOIN achievement a ON pa.AchievementID = a.AchievementID
        WHERE pa.PlayerID = %s
    """
    achievements = execute_query(query, (player_id,))
    
    # Get items
    query = """
        SELECT i.ItemName, i.ItemType, i.Rarity, pi.Quantity, pi.DateObtained
        FROM playeritem pi
        JOIN item i ON pi.ItemID = i.ItemID
        WHERE pi.PlayerID = %s
    """
    items = execute_query(query, (player_id,))
    
    # Get achievement completion
    query = "SELECT fn_achievement_completion(%s) as completion"
    completion = execute_query(query, (player_id,))
    completion_pct = completion[0]['completion'] if completion else 0
    
    return render_template('player_detail.html', 
                         player=player, 
                         achievements=achievements or [],
                         items=items or [],
                         completion=completion_pct)

@app.route('/leaderboard')
def leaderboard():
    """Display leaderboard"""
    connection = get_db_connection()
    if not connection:
        return "Database connection error", 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.callproc('sp_get_leaderboard', [50])
        
        # Fetch results from stored procedure
        results = []
        for result in cursor.stored_results():
            results = result.fetchall()
        
        cursor.close()
        connection.close()
        
        return render_template('leaderboard.html', players=results)
    except Error as e:
        print(f"Error calling stored procedure: {e}")
        return "Error loading leaderboard", 500

@app.route('/games')
def games():
    """Display all games"""
    query = "SELECT * FROM game ORDER BY ReleaseDate DESC"
    games_list = execute_query(query)
    return render_template('games.html', games=games_list or [])

@app.route('/game/<int:game_id>')
def game_detail(game_id):
    """Game detail page"""
    # Get game info
    query = "SELECT * FROM game WHERE GameID = %s"
    game = execute_query(query, (game_id,))
    
    if not game:
        return "Game not found", 404
    
    game = game[0]
    
    # Get levels
    query = """
        SELECT LevelNumber, Difficulty, Description
        FROM level
        WHERE GameID = %s
        ORDER BY LevelNumber
    """
    levels = execute_query(query, (game_id,))
    
    # Get recent sessions
    query = """
        SELECT ms.SessionID, ms.StartTime, ms.EndTime,
               COUNT(ps.PlayerSessionID) as PlayerCount
        FROM multiplayersession ms
        LEFT JOIN playersession ps ON ms.SessionID = ps.SessionID
        WHERE ms.GameID = %s
        GROUP BY ms.SessionID
        ORDER BY ms.StartTime DESC
        LIMIT 10
    """
    sessions = execute_query(query, (game_id,))
    
    return render_template('game_detail.html', 
                         game=game, 
                         levels=levels or [],
                         sessions=sessions or [])

@app.route('/sessions')
def sessions():
    """Display all sessions"""
    query = """
        SELECT ms.SessionID, g.Title as GameTitle, ms.StartTime, ms.EndTime,
               COUNT(ps.PlayerSessionID) as PlayerCount
        FROM multiplayersession ms
        JOIN game g ON ms.GameID = g.GameID
        LEFT JOIN playersession ps ON ms.SessionID = ps.SessionID
        GROUP BY ms.SessionID
        ORDER BY ms.StartTime DESC
        LIMIT 50
    """
    sessions_list = execute_query(query)
    return render_template('sessions.html', sessions=sessions_list or [])

@app.route('/session/<int:session_id>')
def session_detail(session_id):
    """Session detail page"""
    # Get session info
    query = """
        SELECT ms.*, g.Title as GameTitle
        FROM multiplayersession ms
        JOIN game g ON ms.GameID = g.GameID
        WHERE ms.SessionID = %s
    """
    session = execute_query(query, (session_id,))
    
    if not session:
        return "Session not found", 404
    
    session = session[0]
    
    # Get player scores
    query = """
        SELECT ps.Position, p.Username, ps.Score, p.PlayerID
        FROM playersession ps
        JOIN player p ON ps.PlayerID = p.PlayerID
        WHERE ps.SessionID = %s
        ORDER BY ps.Position, ps.Score DESC
    """
    scores = execute_query(query, (session_id,))
    
    return render_template('session_detail.html', 
                         session=session,
                         scores=scores or [])

# =====================================================
# API ENDPOINTS
# =====================================================

@app.route('/api/register', methods=['POST'])
def api_register():
    """API endpoint to register new player"""
    data = request.json
    username = data.get('username')
    email = data.get('email')
    avatar = data.get('avatar', 'default.png')
    
    if not username or not email:
        return jsonify({'error': 'Username and email required'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        cursor.callproc('sp_register_player', [username, email, avatar])
        connection.commit()
        
        # Get the new player ID
        cursor.execute("SELECT LAST_INSERT_ID() as player_id")
        result = cursor.fetchone()
        player_id = result[0] if result else None
        
        cursor.close()
        connection.close()
        
        return jsonify({'success': True, 'player_id': player_id}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/award_item', methods=['POST'])
def api_award_item():
    """API endpoint to award item to player"""
    data = request.json
    player_id = data.get('player_id')
    item_id = data.get('item_id')
    quantity = data.get('quantity', 1)
    
    if not player_id or not item_id:
        return jsonify({'error': 'Player ID and Item ID required'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        cursor.callproc('sp_award_item', [player_id, item_id, quantity])
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({'success': True}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/complete_session/<int:session_id>', methods=['POST'])
def api_complete_session(session_id):
    """API endpoint to complete a session"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = connection.cursor()
        cursor.callproc('sp_complete_session', [session_id])
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({'success': True}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/player_stats/<int:player_id>')
def api_player_stats(player_id):
    """API endpoint for player statistics"""
    stats = {}
    
    # Get achievement completion
    result = execute_query("SELECT fn_achievement_completion(%s) as completion", (player_id,))
    stats['achievement_completion'] = float(result[0]['completion']) if result else 0
    
    # Get inventory count
    result = execute_query("SELECT fn_player_inventory_count(%s) as count", (player_id,))
    stats['inventory_count'] = result[0]['count'] if result else 0
    
    # Get rank
    result = execute_query("SELECT fn_get_player_rank(%s) as rank", (player_id,))
    stats['rank'] = result[0]['rank'] if result else 'Unranked'
    
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
