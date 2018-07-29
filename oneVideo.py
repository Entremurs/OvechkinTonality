# -*- coding: cp1251 -*-

import sys
from Database import Database
from youtube_api_get_comments_from_channel import Video
from youtube_api_get_comments_from_channel import Comments
from apiclient.discovery import build
from apiclient.errors import HttpError
import configOneVideo


YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
DEVELOPER_KEY = 'AIzaSyDTHJ5TDpQ_ixajOM9YbuLcv0oXx0wSpi0'

video = Video()
comments = Comments()

if __name__ == "__main__":

    y = build( YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY )

    try:
        j = 0
        video_comment_threads = comments.get_threads( y, configOneVideo.videolId )
        for thread in video_comment_threads:
            comments.get( y, thread["id"] )
            j+=1
            print j
            # break
        print "-----------DB start------------"
        ODB = Database( configOneVideo.dbName )
        i = 0  # type: int
        #names = [u" "];
        while (i != len( comments.authors )):
            ODB.savetodb( comments.authors[i], comments.text[i], configOneVideo.names )
            # print "qty="+i
            i += 1
        ODB.deinit()

    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)