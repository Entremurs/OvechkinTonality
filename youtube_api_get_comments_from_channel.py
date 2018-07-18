# -*- coding: cp1251 -*-


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
            maxResults=100,
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
            maxResults=100
        ).execute()
        j = 0
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
                maxResults=100
            ).execute()
        print "--------------"
        for item in results["items"]:
            threads.append( item )
            comment = item["snippet"]["topLevelComment"]
            text = comment["snippet"]["textDisplay"]
            self.text.append( text )
            author = comment["snippet"]["authorDisplayName"]
            self.authors.insert( len( self.authors ), author )
        print "Total threads: %d" % len( threads )
        return threads

    def get(self, youtube, parent_id):
        results = youtube.comments().list(
            part="snippet",
            parentId=parent_id,
            maxResults=50,
            textFormat="plainText" ).execute()
        # print parent_id
        for item in results["items"]:
            text = item["snippet"]["textDisplay"]
            author = item["snippet"]["authorDisplayName"]
            self.authors.insert( len( self.authors ), author )
            self.text.append( text )
            # print text
        return results["items"]



