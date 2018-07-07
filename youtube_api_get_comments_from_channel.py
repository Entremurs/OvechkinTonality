# -*- coding: cp1251 -*-
from apiclient.discovery import build
from apiclient.errors import HttpError

from Ovechkin import Database

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
DEVELOPER_KEY = 'AIzaSyDTHJ5TDpQ_ixajOM9YbuLcv0oXx0wSpi0'


class Video():
    def __init__(self):
        self.id_list = []
        self.describ = []
        self.title = []

    def youtube_search(self, youtube, query, ChnlId):
        # Call the search.list method to retrieve results matching the specified
        # query term.
        q = query.decode( 'cp1251' )
        search_response = youtube.search().list(
            q=q,
            part="id,snippet",
            maxResults=50,
            channelId=ChnlId,
            fields='items'
        ).execute()
        for search_result in search_response.get( "items", [] ):
            descr = search_result.get( 'snippet' ).get( 'description' )  # type: object
            title = search_result.get( 'snippet' ).get( 'title' )
            id = search_result.get( 'id' ).get( 'videoId' )
            if id:
                self.id_list.append( id )
                self.describ.append( descr )
                self.title.append( title )
                print title


class Comments():
    def __init__(self):
        self.authors = []
        self.text = []

    def get_threads(self, youtube, video_id):
        threads = []
        results = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
        ).execute()

        for item in results["items"]:
            threads.append( item )
            comment = item["snippet"]["topLevelComment"]
            text = comment["snippet"]["textDisplay"]
            self.text.append( text )
            author = comment["snippet"]["authorDisplayName"]
            self.authors.insert( len( self.authors ), author )

        # Keep getting comments from the following pages
        while ("nextPageToken" in results):
            results = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=results["nextPageToken"],
                textFormat="plainText",
            ).execute()
        print "--------------"
        for item in results["items"]:
            threads.append( item )
            comment = item["snippet"]["topLevelComment"]
            text = comment["snippet"]["textDisplay"]
            self.text.append( text )
            author = comment["snippet"]["authorDisplayName"]
            self.authors.insert( len( comments.authors ), author )
        print "Total threads: %d" % len( threads )
        return threads

    def get(self, youtube, parent_id):
        results = youtube.comments().list(
            part="snippet",
            parentId=parent_id,
            textFormat="plainText" ).execute()
        # print parent_id
        for item in results["items"]:
            text = item["snippet"]["textDisplay"]
            author = item["snippet"]["authorDisplayName"]
            self.authors.insert( len( comments.authors ), author )
            self.text.append( text )
            # print text
        return results["items"]


video = Video()
comments = Comments()

if __name__ == "__main__":

    y = build( YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY )

    try:
        video.youtube_search( y, query="Вашингтон", ChnlId="UCWwCM3cvQjiAecvkph7EyCQ" )
        for vidId in video.id_list:
            video_comment_threads = comments.get_threads( y, vidId )
            for thread in video_comment_threads:
                comments.get( y, thread["id"] )
            # break
        i = 0  # type: int

        ODB = Database( "Ovechkin" )

        ovi_names = [u"Алекс", u"Ови", u"Овечкин", u"Овца", u"Сан", u"Саш", u"великий", u"Великий", u"Барашкин",
                     u"Капитан", u"Овц"]
        while (i != len( comments.authors )):
            ODB.savetodb( comments.authors[i], comments.text[i], ovi_names )
            # print "qty="+i
            i += 1
        ODB.deinit()

    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
