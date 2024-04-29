import json
import math
from collections import defaultdict
from flask import Flask, abort, request
from flask_basicauth import BasicAuth
import pymysql
from requests.auth import HTTPBasicAuth
from flask_swagger_ui import get_swaggerui_blueprint
import getpass


app = Flask(__name__)
app.config.from_file("flask_config.json", load=json.load)
auth = BasicAuth(app)

def remove_null_fields(obj):
    return {k:v for k, v in obj.items() if v is not None}

MAX_PAGE_SIZE = 30
# route detail of person 
@app.route("/person")
@auth.required
def characters():
    page = int(request.args.get('page', 0))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)
    include_details  = bool(int(request.args.get('include_details', 0)))
    
    db_conn = pymysql.connect(host="localhost",
                            user="root", 
                            database="sleep",  
                            password = "-1Xy781227@",
                            cursorclass=pymysql.cursors.DictCursor)

    # Get person 
    with db_conn.cursor() as cursor:
        cursor.execute("""
                    SELECT * FROM sleep.person
                    LIMIT %s
                    OFFSET %s; 
                    """ , (page_size, page * page_size))
        person = cursor.fetchall()
        personid= [per['person_id'] for per in person]

    with db_conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM person")
        total = cursor.fetchone()
        last_page = math.ceil(total['total'] / page_size)
        

    if include_details:
    # Get quality sleep  
        with db_conn.cursor() as cursor:
            placeholder = ','.join(['%s'] * len(personid))
            cursor.execute(f"SELECT * FROM quality_sleep WHERE person_id IN ({placeholder})",
                        personid)
            quality  = cursor.fetchall()
        quality_dict = defaultdict(list)
        for obj in quality:
            name = obj['person_id']
            del obj['person_id']
            quality_dict[name].append(obj)
    
        # Merge quality into person 
        for per in person:
            name = per['person_id']
            per['quality_sleep'] = quality_dict[name]
        
    db_conn.close()
    return {
        'person': person,
        'next_page': f'/person?page={page+1}&page_size={page_size}&include_details={int(include_details)}',
        'last_page': f'/person?page={last_page}&page_size={page_size}&include_details={int(include_details)}',
    }

# Route to specify person_id 
@app.route("/person/<int:person_id>")
def person(person_id):
    
    db_conn = pymysql.connect(host="localhost",
                            user="root", 
                            database="sleep",  
                            password = "-1Xy781227@",
                            cursorclass=pymysql.cursors.DictCursor)


    with db_conn.cursor() as cursor:
        cursor.execute("""
select p.person_id, p.gender, p.age, p.occupation , f.stress_level, f.physical_activity_level , f.daily_steps , f.heart_rate , f.blood_pressure_class , bm.category as bmi ,q.sleep_duration , q.quality_of_sleep ,q.sleep_disorder
from person p
inner join quality_sleep q on p.person_id = q.person_id
inner join factors f on p.person_id = f.person_id 
inner join bmi_index bm on bm.id_bmi = f.id_bmi
            WHERE p.person_id = %s
        """, (person_id,))
        perso = cursor.fetchone()
        if not perso:
            abort(404)
            
    db_conn.close()
    return perso

@app.route("/quality_sleep")
def quality ():
    
    db_conn = pymysql.connect(host="localhost",
                            user="root", 
                            database="sleep",  
                            password = "-1Xy781227@",
                            cursorclass=pymysql.cursors.DictCursor)


    with db_conn.cursor() as cursor:
        cursor.execute("""
select * from quality_sleep
            
        """,)
        quality  = cursor.fetchall()
    db_conn.close()
    return quality 

# Route quality and hours of sleep according to BMI 
@app.route("/quality_sleep/bmi")
def bmi ():
    
    db_conn = pymysql.connect(host="localhost",
                            user="root", 
                            database="sleep",  
                            password = "-1Xy781227@",
                            cursorclass=pymysql.cursors.DictCursor)


    with db_conn.cursor() as cursor:
        cursor.execute("""
SELECT bi.category, ROUND(AVG(qs.quality_of_sleep),2) AS quality_sleep, ROUND(AVG(qs.sleep_duration), 2) AS sleep_duration
FROM quality_sleep qs
INNER JOIN factors f ON f.person_id = qs.person_id
INNER JOIN bmi_index bi ON bi.id_bmi = f.id_bmi
GROUP BY bi.category;
            
        """,)
        bmi  = cursor.fetchall()
    db_conn.close()
    return bmi 

@app.route("/quality_sleep/occupation")
def occupation ():
    
    db_conn = pymysql.connect(host="localhost",
                            user="root", 
                            database="sleep",  
                            password = "-1Xy781227@",
                            cursorclass=pymysql.cursors.DictCursor)

# Route quality and hours of sleep according to occupation and stess level 
    with db_conn.cursor() as cursor:
        cursor.execute("""
SELECT p.occupation, ROUND(AVG(f.stress_level),2) as avg_stress_level, ROUND(AVG(qs.quality_of_sleep),2) AS quality_sleep, ROUND(AVG(qs.sleep_duration), 2) AS sleep_duration
FROM person p
JOIN quality_sleep qs ON p.person_id = qs.person_id
JOIN factors f ON p.person_id = f.person_id
GROUP BY p.occupation;
            
        """,)
        occupation  = cursor.fetchall()
    db_conn.close()
    return occupation 


