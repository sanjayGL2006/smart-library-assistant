import sqlite3
conn = sqlite3.connect('olmspythondb.sqlite3')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS knowledge_knowledgechunk')
cursor.execute('DROP TABLE IF EXISTS knowledge_knowledgedocument')
cursor.execute('DROP TABLE IF EXISTS knowledge_documentchunk')
cursor.execute('DROP TABLE IF EXISTS knowledge_document')
cursor.execute("DELETE FROM django_migrations WHERE app='knowledge'")
conn.commit()
