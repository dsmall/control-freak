import httplib
import xml.dom.minidom

def _getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def getHeadlines(feed):
    feeds = [ '', '/world', '/uk', '/world/us_and_canada', '/science_and_environment',
        '/technology', '/entertainment_and_arts', '/business', '/system/latest_published_content' ]
    conn = httplib.HTTPConnection('feeds.bbci.co.uk')
    conn.request("GET", "/news" + feeds[feed] + "/rss.xml")
    r1 = conn.getresponse()
    print '## getHeadlines ## {0} {1} {2}'.format(feeds[feed], r1.status, r1.reason)
    data1 = r1.read()
    conn.close()
    dom = xml.dom.minidom.parseString(data1)
    items = dom.getElementsByTagName("item")
    headlines = []
    count = 1
    for item in items:
        title = item.getElementsByTagName("title")[0]
        try:
            strTitle = _getText(title.childNodes)
        except:
            strTitle = ''
        description = item.getElementsByTagName("description")[0]
        try:
            strDescription = _getText(description.childNodes)
        except:
            strDescription = ''
        link = item.getElementsByTagName("link")[0]
        try:
            strLink = _getText(link.childNodes)
        except:
            strLink = ''
        pubDate = item.getElementsByTagName("pubDate")[0]
        try:
            strPubDate = _getText(pubDate.childNodes)
        except:
            strPubDate = ''
        if strTitle != '' and strDescription != '' and strLink != '':
            dictItem = {}
            dictItem['title'] = strTitle
            dictItem['description'] = strDescription
            dictItem['link'] = strLink
            dictItem['pubDate'] = strPubDate
            headlines.append(dictItem)
        if len(headlines) >= 15:
            break
        count += 1
        if count >= 20:
            headlines = [ { 'title' : 'News not available' } ]
            break
    return headlines
