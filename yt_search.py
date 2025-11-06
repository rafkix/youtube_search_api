# api/yt_search.py
import json
from yt_dlp import YoutubeDL

class YoutubeSearch:
     def __init__(self, search_terms: str, max_results: int = 40):
          self.search_terms = search_terms
          self.max_results = max_results
          self.videos = []

     async def fetch_results(self):
          ydl_opts = {
               'quiet': True,
               'extract_flat': True,
               'forcejson': True,
               'skip_download': True,
               'default_search': 'ytsearch{}'.format(self.max_results),
          }

          with YoutubeDL(ydl_opts) as ydl:
               search_query = f"ytsearch{self.max_results}:{self.search_terms}"
               info = ydl.extract_info(search_query, download=False)
               self.videos = info.get('entries', [])

     async def to_dict(self, clear_cache=True):
          result = self.videos
          if clear_cache:
               self.videos = []
          return result

     async def to_json(self, clear_cache=True):
          result = json.dumps({"videos": self.videos}, ensure_ascii=False, indent=2)
          if clear_cache:
               self.videos = []
          return result

# async def main():
#      search = YoutubeSearch("Ummon", max_results=40)
#      await search.fetch_results()
#      result = await search.to_dict()
#      print({result[0]['title']})

# if __name__ == "__main__":
#      import asyncio
#      asyncio.run(main())