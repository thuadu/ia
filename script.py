import csv
import pycurl
import certifi
from io import BytesIO
from bs4 import BeautifulSoup
import re


header = 0
with open('training.csv',newline='') as csvfile:
    with open('training3.csv', 'w') as f:
        reader = csv.DictReader(csvfile, delimiter=',')
        c = pycurl.Curl()
        diseases = dict()
        labels = ['209900', '203300', '601626']
        fieldnames = ['Disease', 'Name', 'Sequence']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not header: 
            writer.writeheader()
            header = 1
        for row in reader:
            found_disease = 0
            id = row['Name'].split('.')[0]
            print(id)
            buffer = BytesIO()
            url = "http://h-invitational.jp/hinv/spsoup/transcript_view?hit_id={}&status=disease".format(id)
            #initializing the request URL
            c.setopt(c.URL, url)
            #setting options for cURL transfer  
            c.setopt(c.WRITEDATA, buffer)
            #setting the file name holding the certificates
            # c.setopt(c.CAINFO, certifi.where())
            # perform file transfer
            c.perform()
            #Ending the session and freeing the resources
            soup = BeautifulSoup(buffer.getvalue().decode('iso-8859-1'), 'lxml')
            for p in soup.find_all('td'):
                if not "Disease name" in p.text:
                    continue
                found_disease = 1
                key = p.get_text(strip=True).replace('\r','').replace('\t', '').replace('\n', '').split(';')
                for subkey in key:
                    if subkey == '': continue
                    name = subkey.split(":")[1]
                    pattern = re.compile(r"\((\d+)\)")
                    omim_ids = pattern.findall(name)
                    if len(omim_ids): omim_id = omim_ids[0]
                    else: 
                        writer.writerow({'Disease': 'NA', 'Name': row['Name'], 'Sequence': row['Sequence']})
                        continue
                    if omim_id not in labels: 
                        writer.writerow({'Disease': 'NA', 'Name': row['Name'], 'Sequence': row['Sequence']})
                        continue
                    # if omim_id in diseases:
                    #     diseases[omim_id] = diseases[omim_id] + 1
                    # else:
                    #     diseases[f'name_{omim_id}'] = name 
                    #     diseases[omim_id] = 1
                        
                    # with open("myfile2.txt", 'w') as f: 
                    #     for key, value in diseases.items(): 
                    #         f.write('%s:%s\n' % (key, value))
                    writer.writerow({ 'Disease': name.strip(), 'Name': row['Name'], 'Sequence': row['Sequence']})
            if not found_disease:    
                writer.writerow({'Disease': 'NA', 'Name': row['Name'], 'Sequence': row['Sequence']})
    c.close()