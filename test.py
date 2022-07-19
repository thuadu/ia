import os
import json

DIRECTORY = '/home/antho/Documents/Master/fdi-leex/ia/archive/chest_xray/test/PNEUMONIA'
with open('test.jsonl', 'a+') as file:
    for dirname, _, filenames in os.walk(DIRECTORY):
        for filename in filenames:
            path = os.path.join(DIRECTORY, dirname, filename)
            data = {"content": "gs://anthonytla2/test_pneumonia/"+filename, "mimeType": "image/jpeg"}
            file.write('\n')
            file.write(json.dumps(data))

