from notion_client import AsyncClient
from dotenv import load_dotenv
import asyncio

load_dotenv()
import os
import csv

class LC_2_Anki:
    def __init__(self) -> None:
        self.notion = AsyncClient(auth=os.environ["NOTION_TOKEN"])
    async def extract_documented_questions(self):
        my_page = await self.notion.databases.query(
        **{
            "database_id":os.environ["NOTION_DB"]
        })
        # pprint(my_page['results'])
        self.id_trick = {}
        for i in my_page['results']:
            # print('here')
       
            if i['properties']['Number']['number'] is not None:
                if len(i['properties']['Trick']['rich_text']) > 0:

                    self.id_trick[int(i['properties']['Number']['number'])] = i['properties']['Trick']['rich_text'][0]['plain_text']
                else:
                    self.id_trick[int(i['properties']['Number']['number'])] = ''
    def generate_anki_deck(self):
        result = []
        with open("leetcode.txt") as file:
            tsv_file = csv.reader(file, delimiter="\t")
            for idx, line in enumerate(tsv_file):
                # print(line)
                if idx < 4:
                    result.append(line)
                elif int(line[2]) in self.id_trick.keys():
                    line.append(self.id_trick[int(line[2])])
                    result.append(line)
        with open("deck.tsv", "w") as f:
            writer = csv.writer(f,delimiter='\t')
            writer.writerows(result)
        
            


        


# Note: You can use Markdown! We convert on-the-fly to Notion's internal formatted text data structure.
lc_2_anki = LC_2_Anki()
asyncio.run(lc_2_anki.extract_documented_questions())
lc_2_anki.generate_anki_deck()
