import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime, date
conn=None
# Page configuration
st.set_page_config(
    page_title="Arcade Database Management System",
    page_icon="🎮",
    layout="wide"
)

# Database conn function
@st.cache_resource
def get_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='mini_project_25',
            user='root',
            password='password'  # Update with your MySQL password
        )
        if conn.is_connected():
            return conn
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None
# Initialize connection
conn = get_connection()

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #4ECDC4;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🎮 Arcade Database Management System</h1>', unsafe_allow_html=True)

# Sidebar navigation
menu = st.sidebar.radio(
    "Select Operation",
    [
        "🏠 Home", "➕ Create", "📖 Read",
        "✏️ Update", "🗑️ Delete",
        "🔍 Advanced Queries",
        "⚡ Triggers, Functions & Procedures"
    ]
)

# Helper function
def execute_query(query, params=None, fetch=False):
    global conn
    try:
        # Ensure conn exists or reconnect
        if conn is None or not conn.is_connected():
            conn = get_connection()
            if conn is None or not conn.is_connected():
                st.error("❌ Could not connect to MySQL database.")
                return None

        # Attempt to keep alive
        conn.ping(reconnect=True, attempts=3, delay=2)

        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # FETCH (for SELECT queries)
        if fetch:
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            return pd.DataFrame(result, columns=columns)
        else:
            # Non-select queries (INSERT, UPDATE, DELETE)
            conn.commit()
            cursor.close()
            return True

    except Error as e:
        st.error(f"Database Error: {e}")
        return None

    except Exception as e:
        st.error(f"Unexpected Error: {e}")
        return None

    finally:
        # Safe close even if cursor was never assigned
        try:
            if "cursor" in locals() and cursor:
                cursor.close()
        except:
            pass

# HOME PAGE
if menu == "🏠 Home":
    st.markdown('<h2 class="section-header">Welcome to Arcade Database Management System</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### 📊 Database Statistics")
        if conn:
            players = execute_query("SELECT COUNT(*) as count FROM player", fetch=True)
            games = execute_query("SELECT COUNT(*) as count FROM game", fetch=True)
            st.metric("Total Players", players['count'].iloc[0] if players is not None else 0)
            st.metric("Total Games", games['count'].iloc[0] if games is not None else 0)
    
    with col2:
        st.success("### 🎯 Features")
        st.write("✅ Create new records")
        st.write("✅ Read and view data")
        st.write("✅ Update existing records")
        st.write("✅ Delete records")
        st.write("✅ Advanced queries")
    
    with col3:
        st.warning("### 📋 Tables Available")
        st.write("• Players")
        st.write("• Games")
        st.write("• Achievements")
        st.write("• Items")
        st.write("• Sessions")

# CREATE OPERATIONS
elif menu == "➕ Create":
    st.markdown('<h2 class="section-header">Create New Records</h2>', unsafe_allow_html=True)
    
    create_table = st.selectbox("Select Table", ["Player", "Game", "Achievement", "Item", "Level", "Multiplayer Session", "Rank"])
    
    if create_table == "Player":
        with st.form("create_player"):
            st.subheader("Add New Player")

            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username")
                email = st.text_input("Email")

            with col2:
                avatar = st.text_input("Avatar (optional)", value="default.png")

            submit = st.form_submit_button("Create Player")

            if submit:
                if username and email:
                    # Call stored procedure instead of direct insert
                    try:
                        cursor = conn.cursor()
                        cursor.callproc("sp_register_player", [username, email, avatar])
                        conn.commit()
                        st.success(f"✅ Player '{username}' registered successfully!")

                        # Display assigned PlayerID and Rank
                        df = execute_query("""
                            SELECT PlayerID, Username, TotalScore, 
                                (SELECT RankName FROM ranks WHERE RankID = player.RankID) AS RankName
                            FROM player WHERE Username = %s
                        """, (username,), fetch=True)
                        st.dataframe(df)
                    except Error as e:
                        st.error(f"Error creating player: {e}")
                    finally:
                        cursor.close()
                else:
                    st.warning("⚠️ Please enter both username and email!")

    elif create_table == "Game":
        with st.form("create_game"):
            st.subheader("Add New Game")
            col1, col2 = st.columns(2)
            
            with col1:
                game_id = st.number_input("Game ID", min_value=1, step=1)
                title = st.text_input("Game Title")
                genre = st.selectbox("Genre", ["Arcade", "Action", "RPG", "Strategy", "Sports"])
            
            with col2:
                max_players = st.number_input("Max Players", min_value=1, max_value=100, value=1)
                release_date = st.date_input("Release Date", value=date.today())
            
            submit = st.form_submit_button("Create Game")
            
            if submit:
                query = """INSERT INTO game (GameID, Title, Genre, MaxPlayers, ReleaseDate) 
                           VALUES (%s, %s, %s, %s, %s)"""
                if execute_query(query, (game_id, title, genre, max_players, release_date)):
                    st.success(f"✅ Game '{title}' created successfully!")
    
    elif create_table == "Achievement":
        with st.form("create_achievement"):
            st.subheader("Add New Achievement")
            achievement_id = st.number_input("Achievement ID", min_value=1, step=1)
            name = st.text_input("Achievement Name")
            description = st.text_area("Description")
            
            submit = st.form_submit_button("Create Achievement")
            
            if submit:
                query = """INSERT INTO achievement (AchievementID, Name, Description) 
                           VALUES (%s, %s, %s)"""
                if execute_query(query, (achievement_id, name, description)):
                    st.success(f"✅ Achievement '{name}' created successfully!")
    
    elif create_table == "Item":
        with st.form("create_item"):
            st.subheader("Add New Item")
            col1, col2 = st.columns(2)
            
            with col1:
                item_id = st.number_input("Item ID", min_value=1, step=1)
                item_name = st.text_input("Item Name")
            
            with col2:
                item_type = st.selectbox("Item Type", ["Weapon", "Armor", "Consumable", "Accessory"])
                rarity = st.selectbox("Rarity", ["Common", "Uncommon", "Rare", "Epic", "Mythic"])
            
            submit = st.form_submit_button("Create Item")
            
            if submit:
                query = """INSERT INTO item (ItemID, ItemName, ItemType, Rarity) 
                           VALUES (%s, %s, %s, %s)"""
                if execute_query(query, (item_id, item_name, item_type, rarity)):
                    st.success(f"✅ Item '{item_name}' created successfully!")
    
    elif create_table == "Level":
        with st.form("create_level"):
            st.subheader("Add New Level")
            level_id = st.number_input("Level ID", min_value=1, step=1)
            game_id = st.number_input("Game ID", min_value=1, step=1)
            level_number = st.number_input("Level Number", min_value=1, step=1)
            difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Expert"])
            description = st.text_area("Description")
            
            submit = st.form_submit_button("Create Level")
            
            if submit:
                query = """INSERT INTO level (LevelID, GameID, LevelNumber, Difficulty, Description) 
                           VALUES (%s, %s, %s, %s, %s)"""
                if execute_query(query, (level_id, game_id, level_number, difficulty, description)):
                    st.success(f"✅ Level {level_number} created successfully!")
    
    elif create_table == "Multiplayer Session":
        with st.form("create_session"):
            st.subheader("Add New Multiplayer Session")
            session_id = st.number_input("Session ID", min_value=1, step=1)
            game_id = st.number_input("Game ID", min_value=1, step=1)
            start_time = st.text_input("Start Time (YYYY-MM-DD HH:MM:SS)", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            end_time = st.text_input("End Time (optional, YYYY-MM-DD HH:MM:SS)", value="")
            
            submit = st.form_submit_button("Create Session")
            
            if submit:
                query = """INSERT INTO multiplayersession (SessionID, GameID, StartTime, EndTime) 
                           VALUES (%s, %s, %s, %s)"""
                end_val = end_time if end_time else None
                if execute_query(query, (session_id, game_id, start_time, end_val)):
                    st.success(f"✅ Session {session_id} created successfully!")
    
    elif create_table == "Rank":
        with st.form("create_rank"):
            st.subheader("Add New Rank")
            rank_id = st.number_input("Rank ID", min_value=1, step=1)
            rank_name = st.text_input("Rank Name")
            rank_score = st.number_input("Required Score", min_value=0, step=100)
            
            submit = st.form_submit_button("Create Rank")
            
            if submit:
                query = """INSERT INTO ranks (RankID, RankName, RankScore) 
                           VALUES (%s, %s, %s)"""
                if execute_query(query, (rank_id, rank_name, rank_score)):
                    st.success(f"✅ Rank '{rank_name}' created successfully!")

# READ OPERATIONS
elif menu == "📖 Read":
    st.markdown('<h2 class="section-header">View Database Records</h2>', unsafe_allow_html=True)
    
    read_table = st.selectbox("Select Table to View", 
                              ["Players", "Games", "Achievements", "Items", "Levels", 
                               "Multiplayer Sessions", "Ranks", "Player Achievements", "Player Items"])
    
    if st.button("Load Data", type="primary"):
        if read_table == "Players":
            df = execute_query("""
                SELECT p.PlayerID, p.Username, p.Email, p.RegistrationDate, 
                       p.TotalScore, p.Avatar, r.RankName 
                FROM player p 
                LEFT JOIN ranks r ON p.RankID = r.RankID
            """, fetch=True)
        
        elif read_table == "Games":
            df = execute_query("SELECT * FROM game", fetch=True)
        
        elif read_table == "Achievements":
            df = execute_query("SELECT * FROM achievement", fetch=True)
        
        elif read_table == "Items":
            df = execute_query("SELECT * FROM item", fetch=True)
        
        elif read_table == "Levels":
            df = execute_query("""
                SELECT l.LevelID, l.LevelNumber, l.Difficulty, l.Description, g.Title as GameTitle 
                FROM level l 
                JOIN game g ON l.GameID = g.GameID
            """, fetch=True)
        
        elif read_table == "Multiplayer Sessions":
            df = execute_query("""
                SELECT m.SessionID, g.Title as GameTitle, m.StartTime, m.EndTime 
                FROM multiplayersession m 
                JOIN game g ON m.GameID = g.GameID
            """, fetch=True)
        
        elif read_table == "Ranks":
            df = execute_query("SELECT * FROM ranks ORDER BY RankScore", fetch=True)
        
        elif read_table == "Player Achievements":
            df = execute_query("""
                SELECT p.Username, a.Name as Achievement, a.Description 
                FROM playerachievement pa 
                JOIN player p ON pa.PlayerID = p.PlayerID 
                JOIN achievement a ON pa.AchievementID = a.AchievementID
            """, fetch=True)
        
        elif read_table == "Player Items":
            df = execute_query("""
                SELECT p.Username, i.ItemName, i.ItemType, i.Rarity, 
                       pi.Quantity, pi.DateObtained 
                FROM playeritem pi 
                JOIN player p ON pi.PlayerID = p.PlayerID 
                JOIN item i ON pi.ItemID = i.ItemID
            """, fetch=True)
        
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True, height=400)
            st.info(f"📊 Total Records: {len(df)}")
        else:
            st.warning("⚠️ No data found!")

# UPDATE OPERATIONS
elif menu == "✏️ Update":
    st.markdown('<h2 class="section-header">Update Existing Records</h2>', unsafe_allow_html=True)
    
    update_table = st.selectbox("Select Table to Update", ["Player", "Game", "Achievement", "Item"])
    
    if update_table == "Player":
        st.subheader("Update Player Information")
        
        players_df = execute_query("SELECT PlayerID, Username, Email, TotalScore FROM player", fetch=True)
        if players_df is not None:
            st.dataframe(players_df, use_container_width=True)
        
        with st.form("update_player"):
            player_id = st.number_input("Select Player ID to Update", min_value=1, step=1)
            
            col1, col2 = st.columns(2)
            with col1:
                new_username = st.text_input("New Username (leave empty to keep current)")
                new_email = st.text_input("New Email (leave empty to keep current)")
            with col2:
                new_score = st.number_input("New Total Score (-1 to keep current)", min_value=-1, value=-1)
                new_avatar = st.text_input("New Avatar (leave empty to keep current)")
            
            submit = st.form_submit_button("Update Player")
            
            if submit:
                updates = []
                params = []
                
                if new_username:
                    updates.append("Username = %s")
                    params.append(new_username)
                if new_email:
                    updates.append("Email = %s")
                    params.append(new_email)
                if new_score >= 0:
                    updates.append("TotalScore = %s")
                    params.append(new_score)
                if new_avatar:
                    updates.append("Avatar = %s")
                    params.append(new_avatar)
                
                if updates:
                    params.append(player_id)
                    query = f"UPDATE player SET {', '.join(updates)} WHERE PlayerID = %s"
                    if execute_query(query, tuple(params)):
                        st.success(f"✅ Player ID {player_id} updated successfully!")
                else:
                    st.warning("⚠️ No changes specified!")
    
    elif update_table == "Game":
        st.subheader("Update Game Information")
        
        games_df = execute_query("SELECT GameID, Title, Genre, MaxPlayers FROM game", fetch=True)
        if games_df is not None:
            st.dataframe(games_df, use_container_width=True)
        
        with st.form("update_game"):
            game_id = st.number_input("Select Game ID to Update", min_value=1, step=1)
            new_title = st.text_input("New Title (leave empty to keep current)")
            new_genre = st.selectbox("New Genre", ["", "Arcade", "Action", "RPG", "Strategy", "Sports"])
            new_max_players = st.number_input("New Max Players (-1 to keep current)", min_value=-1, value=-1)
            
            submit = st.form_submit_button("Update Game")
            
            if submit:
                updates = []
                params = []
                
                if new_title:
                    updates.append("Title = %s")
                    params.append(new_title)
                if new_genre:
                    updates.append("Genre = %s")
                    params.append(new_genre)
                if new_max_players > 0:
                    updates.append("MaxPlayers = %s")
                    params.append(new_max_players)
                
                if updates:
                    params.append(game_id)
                    query = f"UPDATE game SET {', '.join(updates)} WHERE GameID = %s"
                    if execute_query(query, tuple(params)):
                        st.success(f"✅ Game ID {game_id} updated successfully!")
                else:
                    st.warning("⚠️ No changes specified!")
    
    elif update_table == "Achievement":
        st.subheader("Update Achievement Information")
        
        ach_df = execute_query("SELECT * FROM achievement", fetch=True)
        if ach_df is not None:
            st.dataframe(ach_df, use_container_width=True)
        
        with st.form("update_achievement"):
            ach_id = st.number_input("Select Achievement ID to Update", min_value=1, step=1)
            new_name = st.text_input("New Name (leave empty to keep current)")
            new_desc = st.text_area("New Description (leave empty to keep current)")
            
            submit = st.form_submit_button("Update Achievement")
            
            if submit:
                updates = []
                params = []
                
                if new_name:
                    updates.append("Name = %s")
                    params.append(new_name)
                if new_desc:
                    updates.append("Description = %s")
                    params.append(new_desc)
                
                if updates:
                    params.append(ach_id)
                    query = f"UPDATE achievement SET {', '.join(updates)} WHERE AchievementID = %s"
                    if execute_query(query, tuple(params)):
                        st.success(f"✅ Achievement ID {ach_id} updated successfully!")
                else:
                    st.warning("⚠️ No changes specified!")
    
    elif update_table == "Item":
        st.subheader("Update Item Information")
        
        items_df = execute_query("SELECT * FROM item", fetch=True)
        if items_df is not None:
            st.dataframe(items_df, use_container_width=True)
        
        with st.form("update_item"):
            item_id = st.number_input("Select Item ID to Update", min_value=1, step=1)
            new_name = st.text_input("New Item Name (leave empty to keep current)")
            new_type = st.selectbox("New Item Type", ["", "Weapon", "Armor", "Consumable", "Accessory"])
            new_rarity = st.selectbox("New Rarity", ["", "Common", "Uncommon", "Rare", "Epic", "Mythic"])
            
            submit = st.form_submit_button("Update Item")
            
            if submit:
                updates = []
                params = []
                
                if new_name:
                    updates.append("ItemName = %s")
                    params.append(new_name)
                if new_type:
                    updates.append("ItemType = %s")
                    params.append(new_type)
                if new_rarity:
                    updates.append("Rarity = %s")
                    params.append(new_rarity)
                
                if updates:
                    params.append(item_id)
                    query = f"UPDATE item SET {', '.join(updates)} WHERE ItemID = %s"
                    if execute_query(query, tuple(params)):
                        st.success(f"✅ Item ID {item_id} updated successfully!")
                else:
                    st.warning("⚠️ No changes specified!")

# DELETE OPERATIONS
elif menu == "🗑️ Delete":
    st.markdown('<h2 class="section-header">Delete Records</h2>', unsafe_allow_html=True)
    st.warning("⚠️ Warning: Deletion is permanent and cannot be undone!")
    
    delete_table = st.selectbox("Select Table", ["Player", "Game", "Achievement", "Item", "Level"])
    
    if delete_table == "Player":
        st.subheader("Delete Player")
        players_df = execute_query("SELECT PlayerID, Username, Email FROM player", fetch=True)
        if players_df is not None:
            st.dataframe(players_df, use_container_width=True)
        
        with st.form("delete_player"):
            player_id = st.number_input("Enter Player ID to Delete", min_value=1, step=1)
            confirm = st.checkbox("I confirm I want to delete this player")
            submit = st.form_submit_button("Delete Player", type="primary")
            
            if submit and confirm:
                query = "DELETE FROM player WHERE PlayerID = %s"
                if execute_query(query, (player_id,)):
                    st.success(f"✅ Player ID {player_id} deleted successfully!")
            elif submit:
                st.error("❌ Please confirm deletion!")
    
    elif delete_table == "Game":
        st.subheader("Delete Game")
        games_df = execute_query("SELECT GameID, Title, Genre FROM game", fetch=True)
        if games_df is not None:
            st.dataframe(games_df, use_container_width=True)
        
        with st.form("delete_game"):
            game_id = st.number_input("Enter Game ID to Delete", min_value=1, step=1)
            confirm = st.checkbox("I confirm I want to delete this game")
            submit = st.form_submit_button("Delete Game", type="primary")
            
            if submit and confirm:
                query = "DELETE FROM game WHERE GameID = %s"
                if execute_query(query, (game_id,)):
                    st.success(f"✅ Game ID {game_id} deleted successfully!")
            elif submit:
                st.error("❌ Please confirm deletion!")
    
    elif delete_table == "Achievement":
        st.subheader("Delete Achievement")
        ach_df = execute_query("SELECT * FROM achievement", fetch=True)
        if ach_df is not None:
            st.dataframe(ach_df, use_container_width=True)
        
        with st.form("delete_achievement"):
            ach_id = st.number_input("Enter Achievement ID to Delete", min_value=1, step=1)
            confirm = st.checkbox("I confirm I want to delete this achievement")
            submit = st.form_submit_button("Delete Achievement", type="primary")
            
            if submit and confirm:
                query = "DELETE FROM achievement WHERE AchievementID = %s"
                if execute_query(query, (ach_id,)):
                    st.success(f"✅ Achievement ID {ach_id} deleted successfully!")
            elif submit:
                st.error("❌ Please confirm deletion!")
    
    elif delete_table == "Item":
        st.subheader("Delete Item")
        items_df = execute_query("SELECT * FROM item", fetch=True)
        if items_df is not None:
            st.dataframe(items_df, use_container_width=True)
        
        with st.form("delete_item"):
            item_id = st.number_input("Enter Item ID to Delete", min_value=1, step=1)
            confirm = st.checkbox("I confirm I want to delete this item")
            submit = st.form_submit_button("Delete Item", type="primary")
            
            if submit and confirm:
                query = "DELETE FROM item WHERE ItemID = %s"
                if execute_query(query, (item_id,)):
                    st.success(f"✅ Item ID {item_id} deleted successfully!")
            elif submit:
                st.error("❌ Please confirm deletion!")
    
    elif delete_table == "Level":
        st.subheader("Delete Level")
        levels_df = execute_query("SELECT l.LevelID, l.LevelNumber, g.Title FROM level l JOIN game g ON l.GameID = g.GameID", fetch=True)
        if levels_df is not None:
            st.dataframe(levels_df, use_container_width=True)
        
        with st.form("delete_level"):
            level_id = st.number_input("Enter Level ID to Delete", min_value=1, step=1)
            confirm = st.checkbox("I confirm I want to delete this level")
            submit = st.form_submit_button("Delete Level", type="primary")
            
            if submit and confirm:
                query = "DELETE FROM level WHERE LevelID = %s"
                if execute_query(query, (level_id,)):
                    st.success(f"✅ Level ID {level_id} deleted successfully!")
            elif submit:
                st.error("❌ Please confirm deletion!")

# ADVANCED QUERIES
elif menu == "🔍 Advanced Queries":
    st.markdown('<h2 class="section-header">Advanced Queries</h2>', unsafe_allow_html=True)
    
    query_type = st.selectbox("Select Query Type", 
                              ["Nested Query - Top Players", 
                               "Join Query - Player Sessions", 
                               "Aggregate Query - Game Statistics"])
    
    if query_type == "Nested Query - Top Players":
        st.subheader("🏆 Players with Above Average Score (Nested Query)")
        st.info("This query finds all players whose total score is above the average score of all players")
        
        if st.button("Execute Query", type="primary"):
            query = """
                SELECT PlayerID, Username, Email, TotalScore, 
                       (SELECT AVG(TotalScore) FROM player) as AverageScore
                FROM player
                WHERE TotalScore > (SELECT AVG(TotalScore) FROM player)
                ORDER BY TotalScore DESC
            """
            df = execute_query(query, fetch=True)
            if df is not None and not df.empty:
                st.dataframe(df, use_container_width=True)
                st.success(f"✅ Found {len(df)} players above average!")
            else:
                st.warning("No results found!")
    
    elif query_type == "Join Query - Player Sessions":
        st.subheader("🎮 Player Session Details (Join Query)")
        st.info("This query joins player, session, and game tables to show detailed session information")
        
        if st.button("Execute Query", type="primary"):
            query = """
                SELECT p.Username, g.Title as GameTitle, 
                       m.StartTime, m.EndTime, ps.Score, ps.Position
                FROM playersession ps
                JOIN player p ON ps.PlayerID = p.PlayerID
                JOIN multiplayersession m ON ps.SessionID = m.SessionID
                JOIN game g ON m.GameID = g.GameID
                ORDER BY ps.Score DESC
            """
            df = execute_query(query, fetch=True)
            if df is not None and not df.empty:
                st.dataframe(df, use_container_width=True)
                st.success(f"✅ Found {len(df)} session records!")
            else:
                st.warning("No results found!")
    
    elif query_type == "Aggregate Query - Game Statistics":
        st.subheader("📊 Game Statistics (Aggregate Query)")
        st.info("This query shows player count, average score, and total score per game")
        
        if st.button("Execute Query", type="primary"):
            query = """
                SELECT g.Title as GameTitle, g.Genre,
                       COUNT(DISTINCT ps.PlayerID) as TotalPlayers,
                       AVG(ps.Score) as AverageScore,
                       SUM(ps.Score) as TotalScore,
                       MAX(ps.Score) as HighScore
                FROM game g
                LEFT JOIN multiplayersession m ON g.GameID = m.GameID
                LEFT JOIN playersession ps ON m.SessionID = ps.SessionID
                GROUP BY g.GameID, g.Title, g.Genre
                ORDER BY TotalPlayers DESC
            """
            df = execute_query(query, fetch=True)
            if df is not None and not df.empty:
                st.dataframe(df, use_container_width=True)
                st.success(f"✅ Statistics for {len(df)} games!")
            else:
                st.warning("No results found!")
    
    # Additional Query Options
    st.markdown("---")
    st.subheader("📝 Custom Query")
    st.warning("⚠️ Advanced users only! Be careful with custom queries.")
    
    custom_query = st.text_area("Enter your SQL query:", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Execute Custom Query"):
            if custom_query:
                df = execute_query(custom_query, fetch=True)
                if df is not None and not df.empty:
                    st.dataframe(df, use_container_width=True)
                    st.success("✅ Query executed successfully!")
                elif df is not None:
                    st.info("Query executed but returned no results")
            else:
                st.error("Please enter a query!")
    
    with col2:
        if st.button("Clear Query"):
            st.rerun()
# DEMO PAGE - Trigger, Function, and Procedure Showcase
elif menu == "⚡ Triggers, Functions & Procedures":
    st.markdown('<h2 class="section-header">⚡ Trigger, Function & Procedure Demo</h2>', unsafe_allow_html=True)
    st.info("Test each stored procedure, trigger, and function interactively using mock data below.")

    choice = st.selectbox(
        "Select Demo:",
        [
            "1️⃣ Register Player (sp_register_player)",
            "2️⃣ Award Item to Player (sp_award_item)",
            "3️⃣ Complete Game Session (sp_complete_session)",
            "4️⃣ Leaderboard Procedure (sp_get_leaderboard)",
            "5️⃣ Trigger: Auto Rank Update",
            "6️⃣ Trigger: Achievement Unlock (First Blood / Sharp Shooter)",
            "7️⃣ Trigger: Validate Item Quantity",
            "8️⃣ Functions Test"
        ]
    )

    # 1️⃣ Register new player (procedure)
    if choice == "1️⃣ Register Player (sp_register_player)":
        username = st.text_input("Username")
        email = st.text_input("Email")
        avatar = st.text_input("Avatar", "avatar_default.png")

        if st.button("Run sp_register_player"):
            try:
                cursor = conn.cursor()
                cursor.callproc("sp_register_player", [username, email, avatar])
                conn.commit()
                st.success(f"✅ Player '{username}' created successfully via procedure.")
                df = execute_query("SELECT * FROM player WHERE Username=%s", (username,), fetch=True)
                st.dataframe(df)
            except Error as e:
                st.error(f"❌ Error: {e}")
            finally:
                cursor.close()

    # 2️⃣ Award item (procedure + trigger)
    elif choice == "2️⃣ Award Item to Player (sp_award_item)":
        players = execute_query("SELECT PlayerID, Username FROM player", fetch=True)
        items = execute_query("SELECT ItemID, ItemName FROM item", fetch=True)

        if players is not None and items is not None:
            player = st.selectbox("Select Player", players["Username"])
            item = st.selectbox("Select Item", items["ItemName"])
            qty = st.number_input("Quantity", min_value=1, max_value=999, value=1)

            # Convert numpy to plain int
            pid = int(players.loc[players["Username"] == player, "PlayerID"].iloc[0])
            iid = int(items.loc[items["ItemName"] == item, "ItemID"].iloc[0])
            qty = int(qty)

            if st.button("Run sp_award_item"):
                try:
                    cursor = conn.cursor()
                    cursor.callproc("sp_award_item", [pid, iid, qty])  # all plain ints now
                    conn.commit()
                    st.success(f"✅ Item '{item}' x{qty} awarded to '{player}' successfully.")
                    df = execute_query("SELECT * FROM playeritem WHERE PlayerID=%s", (pid,), fetch=True)
                    st.dataframe(df)
                except Error as e:
                    st.error(f"❌ Error: {e}")
                finally:
                    cursor.close()
    elif choice == "3️⃣ Complete Game Session (sp_complete_session)":
        sessions = execute_query("SELECT SessionID FROM multiplayersession", fetch=True)
        if sessions is not None and not sessions.empty:
            sid = st.selectbox("Select Session", sessions["SessionID"])
            if st.button("Run sp_complete_session"):
                try:
                    cursor = conn.cursor()
                    # Call procedure
                    cursor.callproc("sp_complete_session", [int(sid)])
                    
                    # Consume all pending result sets (important!)
                    for result in cursor.stored_results():
                        _ = result.fetchall()
                    
                    conn.commit()
                    st.success(f"✅ Session {sid} completed successfully!")

                    # Show updated session details
                    df = execute_query("SELECT * FROM playersession WHERE SessionID=%s", (sid,), fetch=True)
                    st.dataframe(df)
                except Error as e:
                    st.error(f"❌ Error: {e}")
                finally:
                    cursor.close()


    # 4️⃣ Leaderboard
    elif choice == "4️⃣ Leaderboard Procedure (sp_get_leaderboard)":
        top_n = st.number_input("Top N Players", 1, 10, 5)
        if st.button("Run sp_get_leaderboard"):
            df = execute_query(f"CALL sp_get_leaderboard({top_n});", fetch=True)
            st.dataframe(df)

    # 5️⃣ Trigger: Rank auto-update
    def ensure_connection():
        global conn
        if conn is None or not conn.is_connected():
            conn = get_connection()
        try:
            conn.ping(reconnect=True, attempts=3, delay=2)
        except:
            conn = get_connection()
        return conn

    # 5️⃣ Auto Rank Update Trigger
    if choice == "5️⃣ Trigger: Auto Rank Update":
        st.info("Update a player's total score — trigger should auto-adjust their rank.")

        players = execute_query("SELECT PlayerID, Username, TotalScore FROM player", fetch=True)
        if players is not None and not players.empty:
            player = st.selectbox("Select Player", players["Username"])
            pid = int(players.loc[players["Username"] == player, "PlayerID"].iloc[0])
            new_score = st.number_input("New Total Score", min_value=0)

            if st.button("Update Score"):
                try:
                    conn = ensure_connection()
                    cursor = conn.cursor()

                    # Store old rank
                    old_rank = execute_query("SELECT RankID FROM player WHERE PlayerID=%s", (pid,), fetch=True)
                    old_rank_id = old_rank["RankID"].iloc[0] if not old_rank.empty else "?"

                    cursor.execute("UPDATE player SET TotalScore=%s WHERE PlayerID=%s", (new_score, pid))
                    conn.commit()

                    st.success("✅ Score updated successfully! Trigger auto-adjusted rank.")

                    conn.ping(reconnect=True, attempts=3, delay=2)

                    df = execute_query("""
                        SELECT p.Username, p.TotalScore, p.RankID, r.RankName
                        FROM player p 
                        LEFT JOIN ranks r ON p.RankID = r.RankID
                        WHERE p.PlayerID=%s
                    """, (pid,), fetch=True)

                    if not df.empty:
                        new_rank_id = df["RankID"].iloc[0]
                        st.info(f"🏅 Rank changed from {old_rank_id} ➡️ {new_rank_id}")
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.warning("⚠️ Could not fetch updated player info.")

                except Exception as e:
                    st.error(f"❌ Error: {e}")
                finally:
                    try:
                        cursor.close()
                    except:
                        pass

    # 6️⃣ Achievement Unlock Trigger
    elif choice == "6️⃣ Trigger: Achievement Unlock (First Blood / Sharp Shooter)":
        st.info("Insert or update player sessions to trigger achievements automatically.")
        players = execute_query("SELECT PlayerID, Username FROM player", fetch=True)
        sessions = execute_query("SELECT SessionID FROM multiplayersession", fetch=True)

        if players is not None and not players.empty and sessions is not None and not sessions.empty:
            player = st.selectbox("Select Player", players["Username"])
            pid = int(players.loc[players["Username"] == player, "PlayerID"].iloc[0])
            sid = st.selectbox("Select Session", sessions["SessionID"])
            score = st.number_input("Score", min_value=0)

            if st.button("Insert Session Score"):
                try:
                    conn = ensure_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO playersession (SessionID, PlayerID, Score) VALUES (%s, %s, %s)",
                        (sid, pid, int(score))
                    )
                    conn.commit()

                    st.success("✅ Session inserted. Trigger should unlock achievement (if criteria met).")

                    df = execute_query("""
                        SELECT a.Name AS Achievement, a.Description 
                        FROM playerachievement pa
                        JOIN achievement a ON pa.AchievementID = a.AchievementID
                        WHERE pa.PlayerID = %s
                    """, (pid,), fetch=True)

                    if df is not None and not df.empty:
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.warning("⚠️ No achievements yet — try again with a higher score or first session.")

                except Exception as e:
                    st.error(f"❌ Error inserting session: {e}")
                finally:
                    try:
                        cursor.close()
                    except:
                        pass

    # 7️⃣ Validate Item Quantity Trigger
    elif choice == "7️⃣ Trigger: Validate Item Quantity":
        st.info("Try inserting an invalid quantity (<1 or >999) to test validation trigger.")

        players = execute_query("SELECT PlayerID, Username FROM player", fetch=True)
        items = execute_query("SELECT ItemID, ItemName FROM item", fetch=True)

        if players is not None and not players.empty and items is not None and not items.empty:
            player = st.selectbox("Select Player", players["Username"])
            pid = int(players.loc[players["Username"] == player, "PlayerID"].iloc[0])
            item = st.selectbox("Select Item", items["ItemName"])
            iid = int(items.loc[items["ItemName"] == item, "ItemID"].iloc[0])
            qty = st.number_input("Quantity", min_value=-5, max_value=1500, value=0)

            if st.button("Insert PlayerItem"):
                try:
                    conn = ensure_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO playeritem (PlayerID, ItemID, Quantity) VALUES (%s, %s, %s)",
                        (pid, iid, int(qty))
                    )
                    conn.commit()
                    st.success("✅ Insert succeeded (trigger accepted the value).")

                except Error as e:
                    st.error(f"❌ Trigger or DB Error: {e}")
                finally:
                    try:
                        cursor.close()
                    except:
                        pass

    # 8️⃣ Functions Test
    elif choice == "8️⃣ Functions Test":
        st.info("Test all custom MySQL functions for a selected player.")
        players = execute_query("SELECT PlayerID, Username FROM player", fetch=True)

        if players is not None and not players.empty:
            player = st.selectbox("Select Player", players["Username"])
            pid = int(players.loc[players["Username"] == player, "PlayerID"].iloc[0])

            if st.button("Run All Functions"):
                try:
                    conn = ensure_connection()
                    df = execute_query(f"""
                        SELECT 
                            fn_get_player_rank({pid}) AS PlayerRank,
                            fn_achievement_completion({pid}) AS AchievementCompletionPercent,
                            fn_player_inventory_count({pid}) AS TotalInventoryItems,
                            fn_has_achievement({pid}, 1) AS Has_Achievement_1;
                    """, fetch=True)

                    if df is not None and not df.empty:
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.warning("⚠️ No function results returned.")

                except Exception as e:
                    st.error(f"❌ Error executing functions: {e}")
    # 8️⃣ Functions
    elif choice == "8️⃣ Functions Test":
        players = execute_query("SELECT PlayerID, Username FROM player", fetch=True)
        if players is not None:
            player = st.selectbox("Select Player", players["Username"])
            pid = players.loc[players["Username"] == player, "PlayerID"].iloc[0]
            if st.button("Run All Functions"):
                df = execute_query(f"""
                    SELECT 
                        fn_get_player_rank({pid}) AS RankName,
                        fn_achievement_completion({pid}) AS AchievementPercent,
                        fn_player_inventory_count({pid}) AS TotalItems,
                        fn_has_achievement({pid}, 1) AS Has_Achievement_1;
                """, fetch=True)
                st.dataframe(df)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Arcade Database Management System © 2025 | Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)
