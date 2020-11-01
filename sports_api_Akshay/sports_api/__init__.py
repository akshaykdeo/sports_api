
import os

# Import the framework
from flask import Flask, g, request, make_response, jsonify
from flask_restful import Resource, Api,  reqparse
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.dialects.postgresql import JSON, JSONB
from sqlalchemy import func
from sqlalchemy import type_coerce

# Create an instance of Flask
app = Flask(__name__)


# Connect to Postgres database and set connection strings (To connect, use host_name according to service of Docker container)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Postgres24@localhost/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Postgres24@db:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create db instance through SQLAlchemy
db = SQLAlchemy(app)

# Define structure in which you want the table in Postgres DB.
class Sports_data_table(db.Model):
    __tablename__ = 'Sports_data_table'
    id = db.Column(db.BigInteger, primary_key=True)
    message_type = db.Column(db.String())
    startTime = db.Column(db.DateTime)
    event = db.Column(JSONB)
    

# Create the API
api = Api(app)


# Display all objects in Database on index page of Website (This is just to get all the ids in the database and can be changed easily according to requirements)
@app.route("/")
def index():
        
    #Return all objects in Database. Useful to get all the IDs which can used in http://localhost:5000/match/994839351740 to view data
    all_objects = Sports_data_table.query.all()
    all_objects = {"id"+str(i):str(i) for i in all_objects}
    return all_objects


#flask_restful is used which is an extension of FLask which gives some functionalities to create APIs
#Create class for each endpoint
#For each class (endpoint), create method you want to accept (GET,POST)
#There are 2 endpoints-
        #1. /match/ : GET method implementation for the 3 use cases -  Retrieve match by id; Retrieve football matches ordered by start_time; Retrieve matches filtered by name.
        #2. /add : POST method implementation for the 2 use cases - A complete new sporting event is being created; There is an update for the odds field.
        
# Class and method for Endpoint1
class GetMatchData(Resource):
    def get(self,identifier=None):

        #Use Case 1 :Retrieve match by id:
        #request: http://localhost:5000/match/994839351740
        if identifier is not None:
            get_record = Sports_data_table.query.filter_by(id = identifier).first()
            #Return if id does not exist in Database
            if get_record is None:
                return "Record not found", 404
                
            resp=  {
                             "id": identifier,
                             "url": "http://localhost:5000/match/"+str(identifier),
                             "name": get_record.event['name'],
                             "startTime": get_record.event['startTime'],
                             "sport": get_record.event['sport'],
                             "markets": get_record.event['markets']
                    }
            return resp, 200

        
        #Retrieve mentioned arguments to the URL if passed
        sport = request.args.get('sport')
        ordering = request.args.get('ordering')
        name = request.args.get('name')
        
        #Use Case 2 : Retrieve football matches ordered by start_time:
        #request: http://localhost:5000/match/?sport=football&ordering=startTime
        if sport is not None and ordering is not None:
            get_record = Sports_data_table.query.filter(func.lower(Sports_data_table.event['sport']['name'].astext) == func.lower(sport)).order_by(Sports_data_table.startTime).all()
            #Return if not exist in Database
            if len(get_record)==0:
                return "Record not found", 404
            
            ordered_records = []
            for rec in get_record:
                
                ordered_records.append({
                                     "id": rec.id,
                                     "url": "http://localhost:5000/match/"+str(rec.id),
                                     "name": rec.event['name'],
                                     "startTime": rec.event['startTime'],
    
                            })
            return ordered_records, 200
        
        
        #Use Case 3 : Retrieve matches filtered by name:
        #request: http://localhost:5000/match/?name=Real%20Madrid%20vs%20Barcelona
        if name is not None:
            print("name is = ",name)
            get_record = Sports_data_table.query.filter(func.lower(Sports_data_table.event['name'].astext) == func.lower(name)).all()
            #Return if not exist in Database
            if len(get_record)==0:
                return "Record not found", 404
            
            name_records = []
            for rec in get_record:
                
                name_records.append({
                                     "id": rec.id,
                                     "url": "http://localhost:5000/match/"+str(rec.id),
                                     "name": rec.event['name'],
                                     "startTime": rec.event['startTime'],
    
                            })
            return name_records, 200
            
        
        return "Request not found", 400 


# Class and method for Endpoint2
class AddData(Resource):
    def post(self):        
        
#        #Create tables in postgres database for the initial run ( Only if table does'nt already exist in database)
#        db.create_all()
#        db.session.commit()
#        print("table created")
        
        if request.is_json:
            req_data = request.get_json()
            print("req_data type",type(req_data))
            print()
            data_row = Sports_data_table(id = req_data["id"], message_type = req_data["message_type"], startTime = req_data["event"]["startTime"], event = req_data["event"])
            message_type = req_data["message_type"]
            
            #Use Case 4 : A complete new sporting event is being created. Return if id already exists in DB
            if message_type == "NewEvent":
                print("Inside new event")
                try:
                    db.session.add(data_row)
                    db.session.commit()
                    return "Data Inserted", 201
                except Exception as e:
                    return "ID should be unique and already exists. Error : "+str(e), 406
            
            #Use Case 5 : There is an update for the odds field. 
            elif message_type == "UpdateOdds":
                #Retrieve record with the matching id passed through POST from database.
                record = Sports_data_table.query.filter_by(id = req_data["id"]).first()
                
                #Return if id does not exist in Database
                if record is None:
                    return "Record not found", 404
                filter_by_id_base_query =db.session.query(Sports_data_table).filter(Sports_data_table.id == req_data["id"])
                i=0
                
                #After retrieving record with matched id from database, For every selection record in database, find its matching pair from the data received through POST method and update that selection.
                #This is seach by id and hence only those selections->odds are updated whose selection->id matches with ones in our database. Thus, data integrity is maintained and if incorrect (incorrect selection->id) or extra selections are passed through POST request, it will not touch unmatched items. Edge cases can be easily handled in try except blocks, based upon app requirements.
                for selection in record.event["markets"][0]["selections"]:
#                   try:
                    
                    #Will match the selection id with that of the record existing in the database and will get the selections list index matched by the selection id. This index will give the corresponding selection (position) from the received POST request data.
                    #This is a crude approach, but works well as there are few list items in the "selections". Can be replaced by using Table Joins which may be a more efficient approach (Will need to create multiple data stuctures and can increase space complexity.)
                    update_index = next(i for i, item in enumerate(req_data["event"]["markets"][0]["selections"]) if item["id"] == selection["id"])
                    
                    #Get the new odd value of corresponding selection from received POST request data.
                    new_odd = req_data["event"]["markets"][0]["selections"][update_index]["odds"]
                    
                    #Once we get the correct list index of the received POST data matched with selection id from our db, use jsonb_set to update odds value with the new value. Path passed to to jsonb_set will traverse through the json blob (DB Column: event) in the manner {markets,0,selections,"+str(i)+",odds} where i is the index of the current selection id found in our database.
                    filter_by_id_base_query.update({Sports_data_table.event: func.jsonb_set(Sports_data_table.event,"{markets,0,selections,"+str(i)+",odds}",type_coerce(new_odd,JSONB))}, synchronize_session="fetch")
                    db.session.commit()
                    
                    i+=1
                return record.event, 201
#                    except:
#                        return "Could not update as selectionn id not found", 406
                       
  
        else:
            return "Incorrect JSON format", 400


#Adds a resource to the api containing the URLS we want to access.
api.add_resource(GetMatchData, '/match/', '/match/<string:identifier>')

api.add_resource(AddData, '/add')
