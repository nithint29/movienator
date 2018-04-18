import boto3
from time import sleep
from tmdbv3api import TMDb, Movie, Person
from botocore.exceptions import ClientError

def scan_table(table):
    response = table.scan()

    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break

    return items

def append_id(ids,items):
    for item in items:
        ids.append(item['ID'])

def populate_cast(table,ids):
    gd={0:"not set",1:"female",2:"male"} #map of integer to gender
    count=0
    x=0
    for id in ids:
        sleep(0.26)
        credits=movie.credits(id)
        if(hasattr(credits, 'crew')):
            for m in credits.crew:
                #sleep(0.26)
                if(m.get('job') in ("Director", "Producer", "Executive Producer", "Director of Photography", "Screenplay")): 
                    pid=m.get('id') if m.get('id') != '' else None
                    name=m.get('name')   if m.get('name') != '' else None
                    gender=gd[m.get('gender')] if m.get('gender') != '' else None
                    cid=m.get('credit_id') if m.get('credit_id') != '' else None
                    job=m.get('job') if m.get('job') != '' else None
                    dept=m.get('department') if m.get('department') != '' else None
                    profile_path=m.get('profile_path') if m.get('profile_path') != '' else None
                    sleep(0.26)
                    details=person.details(pid)
                    adult=details.adult if hasattr(details,'adult') and details.adult != '' else None
                    aks=[x if x else 'not available' for x in details.also_known_as] if hasattr(details,'also_known_as') and details.also_known_as is not None else None
                    bio=details.biography if hasattr(details,'biography') and details.biography != '' else None
                    bday=details.birthday if hasattr(details,'birthday') and details.birthday != '' else None
                    dday=details.deathday if hasattr(details,'deathday') and details.deathday != '' else None
                    imdb_id=details.imdb_id if hasattr(details,'imdb_id') and details.imdb_id != '' else None
                    home=details.homepage if hasattr(details,'homepage') and details.homepage != '' else None
                    birthplace=details.place_of_birth if hasattr(details,'place_of_birth') and details.place_of_birth != '' else None
                    popularity=str(details.popularity) if hasattr(details,'popularity') and str(details.popularity) != '' else None
                    
                    try:   
                        table.put_item(
                            Item = {
                                'person_id': pid,
                                'name': name,
                                'gender': gender,
                                'adult':adult,
                                'credit_id': cid,
                                'job': job,
                                'department': dept,
                                'profile_path': profile_path,
                                'also_known_as': aks,
                                'biography': bio,
                                'birthday': bday,
                                'deathday': dday,
                                'imdb_id': imdb_id,
                                'homepage': home,
                                'place_of_birth': birthplace,
                                'popularity': popularity
                            },
                            ConditionExpression='attribute_not_exists(person_id)'
                        )
                    except ClientError as e:
                        # Ignore the ConditionalCheckFailedException, bubble up
                        # other exceptions.
                        if e.response['Error']['Code'] != 'ConditionalCheckFailedException': raise
        else:
            print(id)

if __name__ == "__main__":
    dynamodb = boto3.resource('dynamodb')
    moviesnew = dynamodb.Table('movies_new')
    crew = dynamodb.Table('crew')

    tmdb = TMDb()
    movie = Movie()
    person = Person()

    tmdb.api_key='a334426826809d332101199d1acebb0f'

    items=scan_table(moviesnew)

    ids=[]
    append_id(ids,items)

    populate_cast(crew,ids)