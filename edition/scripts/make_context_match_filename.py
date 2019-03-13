"""
The verses in the critical edition come from the context value in the collations
so we need to make sure that agrees with the file name as there have been some
changes of numbering during the life of the project.


"""
import os
import json

directory = '../../collation/approved'

for file in os.listdir(directory):
    if file.endswith('.json'):        
        filename = os.path.join(directory, file)
        with open(filename) as file_p:
            data = json.load(file_p)
            data['context'] = file.replace('.json', '')
        with open(filename, 'w') as file_out:
            json.dump(data, file_out, ensure_ascii=False, indent=4)
        