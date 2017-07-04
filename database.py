import os

import pymysql

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')


def get_connection():
    return pymysql.connect(host=DB_HOST,
                           user=DB_USER,
                           password=DB_PASSWORD,
                           db=DB_NAME,
                           charset='utf8',)


def get_all_movies():
    conn = get_connection()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT * FROM movie'
    curs.execute(sql)
    rows = curs.fetchall()
    conn.close()
    return rows


def get_movies_by_genre(genre):
    conn = get_connection()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT * FROM movie WHERE genre LIKE %s'
    curs.execute(sql, ('%'+genre+'%',))
    rows = curs.fetchall()
    conn.close()
    return rows


def get_movies_by_genre(genre):
    conn = get_connection()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT * FROM movie WHERE genre LIKE %s'
    curs.execute(sql, ('%'+genre+'%',))
    rows = curs.fetchall()
    conn.close()
    return rows


def get_movies_by_actor(actor):
    conn = get_connection()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT * FROM movie WHERE actor LIKE %s'
    curs.execute(sql, ('%'+actor+'%',))
    rows = curs.fetchall()
    conn.close()
    return rows


def get_movies_by_director(director):
    conn = get_connection()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'SELECT * FROM movie WHERE director LIKE %s'
    curs.execute(sql, ('%'+director+'%',))
    rows = curs.fetchall()
    conn.close()
    return rows


def add_movie(naver_code, kor_title, eng_title, genre, director, actor):
    conn = get_connection()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'INSERT INTO movie(naver_code, kor_title, eng_title, genre, director, actor) VALUES(%s, %s, %s, %s, %s, %s)'
    data = (naver_code, kor_title, eng_title, genre, director, actor,)
    result = curs.execute(sql, data)
    conn.commit()
    conn.close()
    return result
