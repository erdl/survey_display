#!/usr/bin/env python3
import psycopg2 as psql
import src.utils.files as futils

# This is the primary `inner-join` used to collect the goods.
CMD = """
    SELECT
      "public".kiosk_survey.url,
      "public".kiosk_survey.survey_info_id,
      "public".survey_question.question_id,
      "public".survey_question.question_position,
      "public".question.question_text,
      "public"."option".option_id,
      "public"."option"."text"
    FROM "public".kiosk_survey
    INNER JOIN "public".survey_question
      ON "public".kiosk_survey.survey_info_id = "public".survey_question.survey_info_id
    INNER JOIN "public".question
      ON "public".survey_question.question_id = "public".question.question_id
    INNER JOIN "public"."option"
      ON "public"."option".question_id = "public".question.question_id
    """
# the field layout returned by the above `inner-join`.
FIELDS = ["url","survey-id","question-id","question-ord","question-txt","option-id","option-txt"]


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
    config = load_config('psql')
    db = config['settings']['database']
    raw = execute(db,CMD)
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
        survey = mapping.get(url,{'id':row['survey-id'],'questions':[]})
        # filter `questions` to see if corresponding question object exists.
        fltr = lambda q: q['id'] == row['question-id']
        match = [(i,q) for i,q in enumerate(survey['questions']) if fltr(q)]
        assert len(match) <= 1
        # get question object & index, or initialize a new question object.
        index,question = match.pop() if match else (None,init_question(row))
        # add the new option object to the `options` field.
        option = {'id':row['option-id'],'txt':row['option-txt']}
        question['options'].append(option)
        # insert or append the question object as appropriate.
        if isinstance(index,int):
            survey['questions'][index] = question
        else: survey['questions'].append(question)
        # overwrite/add the survey object to the `mapping`.
        mapping[url] = survey
    return mapping

# initialize a new question object from
# a given dictionary of values.
def init_question(spec):
    question = { 'options': [] }
    question['id'] = spec['question-id']
    question['txt'] = spec['question-txt']
    question['ord'] = spec['question-ord']
    return question

# execute a given psql command & return results.
def execute(db,cmd):
    con = psql.connect(database=db)
    cur = con.cursor()
    cur.execute(cmd)
    data = cur.fetchall()
    con.close()
    return data
