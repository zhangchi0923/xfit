from flask import Flask, jsonify, request
import pymysql
import Logger
from settings import *

app = Flask(__name__)

def connect_db():
    """Connect to the database."""
    db_connection = pymysql.connect(
    host='gz-cynosdbmysql-grp-80f3rbb1.sql.tencentcdb.com',
    port=25752,
    user='root',
    passwd='Drbrain123',
    db='boxing'
    )
    return db_connection

logger = Logger.Logger(LOG_FILE_PATH).create_logger()

@app.route('/v1/enter_main_window', methods=['POST'])
def enter_main_window():
    try:
        # Retrieve sign up data from request
        data = request.get_json(force=True)
        username = data['username']

        # Connect to the database
        with connect_db() as conn:
            logger.info('Connected to the database.')
            cur = conn.cursor()
            # Check if the user already exists
            cur.execute('SELECT user_id from user WHERE user_name = %s', (username))
            result = cur.fetchall()
            if not result:
                '''user not exist and sign up'''
                cur.execute('INSERT INTO user (user_name) VALUES (%s)', (username))
                conn.commit()
                logger.info('Username ({})- {} not exist but successfully registered.'.format(username, cur.lastrowid))
                return jsonify({'success': True, 'message': 'Username successfully registered', 'user_id':cur.lastrowid})
            logger.info('Username ({})- {} signed in.'.format(username, result[0][0]))
        return jsonify({'success': True, 'message': 'User successfully signed in', 'user_id':result[0][0]})
    except Exception as e:
        logger.error('Error: {}'.format(str(e)))
        return jsonify({'success': False, 'message': str(e), 'user_id':None})

@app.route('/v1/start_game', methods=['POST'])
def start_game():
    try:
        # Retrieve params from request
        data = request.get_json(force=True)
        song_id = data['song_id']
        logger.info('User start game with song_id: {}'.format(song_id))
        # Connect to the database
        with connect_db() as conn:
            logger.info('Connected to the database.')
            cur = conn.cursor()
            '''Get all scores of this song'''
            cur.execute('SELECT user_name, score from play_record WHERE song_id = %s', (song_id))
            result = cur.fetchall()
        logger.info('Rank info of song-{} sent.'.format(song_id))
        return jsonify({'success': True, 'message': 'Rank info sent.', 'rank':result})
    except Exception as e:
        logger.error('Error: {}'.format(str(e)))
        return jsonify({'success': False, 'message': str(e)})

@app.route('/v1/end_game', methods=['POST'])
def end_game():
    try:
        # Retrieve params from request
        data = request.get_json(force=True)
        user_id = data['user_id']
        user_name = data['user_name']
        song_id = data['song_id']
        start_time = data['start_time']
        end_time = data['end_time']
        score = data['score']
        combo = data['combo']

        # Connect to the database
        with connect_db() as conn:
            logger.info('Connected to the database.')
            cur = conn.cursor()
            '''insert play_record'''
            # get user_name
            cur.execute('INSERT INTO play_record (play_start_time, play_end_time, song_id, user_id, score, combo, user_name) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (start_time, end_time, song_id, user_id, score, combo, user_name))
            
            '''update user status'''
            cur.execute('UPDATE user SET play_times=play_times + 1, end_time_last_play=%s, song_id_last_play=%s WHERE user_id = %s',
                         (end_time, song_id, user_id))
            logger.info('Play record of song-{} user-{} updated successfully.'.format(song_id, user_id))

            '''update song status'''
            # retrieve highest score and highest combo
            cur.execute('SELECT highest_score, highest_combo FROM song WHERE song_id = %s', (song_id))
            # print(cur.fetchall())
            max_score, max_combo = cur.fetchall()[0]
            if score > max_score and combo > max_combo:
                cur.execute(
                    'UPDATE song SET play_times = play_times+1, highest_score = %s, highest_combo = %s, end_time_last_play = %s, user_id_highest_score = %s, user_id_highest_combo = %s, end_time_highest_score = %s, end_time_highest_combo = %s WHERE song_id = %s',
                    (score, combo, end_time, user_id, user_id, end_time, end_time, song_id)
                )
            elif score > max_score:
                cur.execute(
                    'UPDATE song SET play_times = play_times+1, highest_score = %s, end_time_last_play = %s, user_id_highest_score = %s, end_time_highest_score = %s WHERE song_id = %s',
                    (score, end_time, user_id, end_time, song_id)
                )
            elif combo > max_combo:
                cur.execute(
                    'UPDATE song SET play_times = play_times+1, highest_combo = %s, end_time_last_play = %s, user_id_highest_combo = %s, end_time_highest_combo = %s WHERE song_id = %s',
                    (combo, end_time, user_id, end_time, song_id)
                )
            else:
                cur.execute(
                    'UPDATE song SET play_times = play_times+1, end_time_last_play = %s WHERE song_id = %s',
                    (end_time, song_id)
                )
            logger.info('Song-{} status updated successfully.'.format(song_id))
            conn.commit()
            logger.info('Changes committed.')
            # result = cur.fetchall()
            
        return jsonify({'success': True, 'message': 'Information updated.', 'body':None})
    except Exception as e:
        logger.error('Error: {}'.format(str(e)))
        return jsonify({'success': False, 'message': str(e)})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8082, debug=True)