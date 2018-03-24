#!/usr/bin/env python3
import psycopg2 as psql
from . import files as futils
from .. import appconf

CONFIG = appconf.get('psql',{})

# This is the primary `inner-join` used to collect the goods.
CMD = """
    SELECT
    "public".kiosk_survey.url,
    "public".kiosk_survey.survey_info_id,
    "public".survey_question.question_id,
    "public".survey_question.question_position,
    "public".question.question_text,
    "public"."option".option_id,
    "public"."option"."text",
    "public".kiosk_survey.deployed_url_id,
    "public".deployed_url.is_kiosk,
    "public"."option"."option_color"
    FROM
    "public".kiosk_survey
    INNER JOIN "public".survey_question ON "public".kiosk_survey.survey_info_id = "public".survey_question.survey_info_id
    INNER JOIN "public".question ON "public".survey_question.question_id = "public".question.question_id
    INNER JOIN "public"."option" ON "public"."option".question_id = "public".question.question_id
    INNER JOIN "public".deployed_url ON "public".kiosk_survey.deployed_url_id = "public".deployed_url.deployed_url_id
    ORDER BY
    "public"."option"."response_position"
    """
# the field layout returned by the above `inner-join`.
FIELDS = ["url","survey-id","question-id","question-ord","question-txt","option-id","option-txt", "url-id","is-kiosk", "option_color"]


# deployment model:
# ----------------
#   "url" : {
#     "id" : Int,
#     "questions": [
#       { "txt": String, "id": Int, "ord": Int
#       , "options": [ {"txt": String, "id": Int}, ... ]
#       }, ...
#     ]
#   }
# ----------------


# load all currently active deployments.
def load_active():
    if not 'database' in CONFIG: return {}
    raw = execute(CMD)
    active = parse_active(raw)
    return active


# construct a series of deployment objects
# based upon a set of raw SQL rows.
def parse_active(rows):
    mapping = {}
    for row in rows:
        # convert row to dict using the FIELDS variable to
        # match field names to their given indexes.
        row = {k: row[i] for i,k in enumerate(FIELDS)}
        url = row['url']
        # extract the survey for the given url, or supply
        # a new survey object if none yet exists.
        spec = mapping.get(url,{'is-kiosk': bool(row['is-kiosk']),'url-id': row['url-id']})
        survey = spec.get('survey',{'code':row['survey-id'],'itms':[]})
        # filter `questions` to see if corresponding question object exists.
        fltr = lambda q: q['code'] == row['question-id']
        match = [(i,q) for i,q in enumerate(survey['itms']) if fltr(q)]
        assert len(match) <= 1
        # get question object & index, or initialize a new question object.
        index,question = match.pop() if match else (None,init_question(row))
        # add the new option object to the `options` field.
        option = {'code':row['option-id'],'text':row['option-txt'], 'option_color':row['option_color']}
        question['opts'].append(option)
        # insert or append the question object as appropriate.
        if isinstance(index,int):
            survey['itms'][index] = question
        else: survey['itms'].append(question)
        # overwrite/add the survey object to the `mapping`.
        spec['survey'] = survey
        mapping[url] = spec
    for name,spec in mapping.items():
        survey = spec['survey']
        survey['text'] = name
        survey['itms'] = sorted(survey['itms'],key = lambda itm: itm['ord'])
        for itm in survey['itms']:
            _ = itm.pop('ord')
        spec['survey'] = survey
    return mapping

# initialize a new question object from
# a given dictionary of values.
def init_question(spec):
    question = { 'opts': [] }
    question['code'] = spec['question-id']
    question['text'] = spec['question-txt']
    question['ord'] = spec['question-ord']
    return question

# execute a given psql command & return results.
def execute(cmd):
    if not "database" in CONFIG:
        raise Exception("no value for `database` in `psql` configuration!")
    keys = ("user","host","password","database")
    conf = { key : CONFIG[key] for key in keys if key in CONFIG }
    con = psql.connect(**conf)
    cur = con.cursor()
    cur.execute(cmd)
    data = cur.fetchall()
    con.close()
    return data

# check to see if a given survey has been set to active via survey_admin
def is_active(url):
    
    # get possible URLS that are active
    get_url_query = "SELECT url_text FROM deployed_url WHERE is_active = TRUE"
    
    if not "database" in CONFIG:
        raise Exception("no value for `database` in `psql` configuration!")
    keys = ("user","host","password","database")
    conf = { key : CONFIG[key] for key in keys if key in CONFIG }
    con = psql.connect(**conf)
    cur = con.cursor()
    cur.execute(get_url_query)
    
    deployed_url_list = [x[0] for x in cur.fetchall()]

    con.close()
    # see if url string is in the result of the query
    # use this to avoid allowing user input to avoid any type of sql injection
    try:
        deployed_url_list.index(url)
        return True
    except ValueError:
        return False

    # if it isn't then return false to redirect user to some default page





    
