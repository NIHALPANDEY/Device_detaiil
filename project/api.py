import pandas as pd
import redis
import json

redis_instance = redis.StrictRedis(host='redis',
                                  port=6379, db=0, decode_responses=True)
                    
data = pd.read_csv('sample.csv')
sorted_data = data.sort_values(by=['sts'])
data = sorted_data.to_dict('records')
for row in data:
    value = redis_instance.get(row.get('device_fk_id'))
    key_data = eval(value) if value else []
    key_data.append(row)
    redis_instance.set(row.get('device_fk_id'), json.dumps(key_data))
    
    
    


