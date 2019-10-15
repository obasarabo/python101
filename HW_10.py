import sqlite3
import os
import csv

def sql_connection(db_file):
    if os.path.isfile(db_file):os.remove(db_file) #delete DB if exists
    conn = sqlite3.connect(db_file)
    return(conn)

def sql_create(conn,create_sql):
    curs=conn.cursor()
    curs.execute(create_sql)

def sql_insert(conn,insert_sql,values):
    curs=conn.cursor()
    curs.executemany(insert_sql,values)

def sql_read(conn,sql_select):
    curs=conn.cursor()
    curs.execute(sql_select)
    records = curs.fetchall()
    for row in records:
        print(row)

sql_create_project_table = """ CREATE TABLE IF NOT EXISTS Project (
                                        Name text NOT NULL,
                                        description text NOT NULL,
                                        deadline date                                    
                                    ); """

sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS Tasks (
                                    id number PRIMARY KEY,
                                    priority integer NOT NULL,
                                    details text NOT NULL,
                                    status text NOT NULL,
                                    deadline date NOT NULL,
                                    completed date,
                                    project text,
                                    FOREIGN KEY (project) REFERENCES Project (Name)
                                );"""
sql_insert_into_project = """INSERT INTO 'Project' 
                            ('Name','description','deadline')
                            VALUES (?,?,?)
                            ;"""
sql_insert_into_tasks = """INSERT INTO 'Tasks'
                        ('id', 'priority','details','status', 'deadline', 'completed', 'project')
                        VALUES(?,?,?,?,?,?,?)
                        ;"""
sql_select = """Select * from Tasks t left join Project p on t.project=p.Name"""

if __name__== "__main__":
    db=sql_connection("D:\\test.db")
    #Creating tables
    sql_create(db,sql_create_project_table)
    sql_create(db,sql_create_tasks_table)
    
    #Filling tables with data from csv files
    with open('D:\\Tasks.csv') as tasks_csv:
        tasks = csv.DictReader(tasks_csv)
        to_tasks = [(i['ID'], i['Priority'],i['Details'],i['Status'], i['Deadline'], i['Completed'], i['Project']) for i in tasks]
    with open('D:\\Project.csv') as project_csv:
        project = csv.DictReader(project_csv)
        to_project = [(i['Name'], i['Description'],i['Dealine']) for i in project]
    sql_insert(db,sql_insert_into_tasks,to_tasks)
    sql_insert(db,sql_insert_into_project,to_project)
    
    #Printing selected data
    sql_read(db,sql_select)
