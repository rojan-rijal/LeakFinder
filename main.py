import sys
from helpers import sendRequest, getWebsiteTitle, runTrelloApi, sendToUrlScan
from time import sleep
# global arrays for what the search should have
trello = []
googleProductForums = []
prezi = []
bookmarks = []
codepen = []
misc = []


def resultSort(results, url): #results in an array
    trello.clear()
    prezi.clear()
    bookmarks.clear()
    codepen.clear()
    googleProductForums.clear()
    results = results
    totalResults = int(results['queries']['request'][0]['totalResults'])
    totalScanNeeded = totalResults / 10
    startCount = 1
    requestSend = 1
    while startCount <= totalScanNeeded+1:
        for data in results['items']:
            if "trello.com" in data['link']:
                trello.append(data['link'])
            elif "prezi.com" in data['link']:
                prezi.append(data['link'])
            elif "productforums.google.com" in data['link']:
                googleProductForums.append(data['link'])
            elif "codepen.io" in data['link']:
                codepen.append(data['link'])
            elif "papaly.com" in data["link"]:
                bookmarks.append(data["link"])
        startCount+=1
        if requestSend+10 > totalResults:
            requestSend = requestSend
        else:
            requestSend += 10
        results = sendRequest(url, requestSend)




def main(url):
	search_result = sendRequest(url, 1)
	resultSort(search_result,url)
	filename = '{0}.md'.format(url)
	with open(filename, 'a') as report:
		report.write('--------\n')
		report.write('weakness: Information Disclosure\n')
		report.write('--------\n')
		report.write('# LeakFinder Result for {0} \n'.format(url))
		if len(trello) > 0:
			trelloInfos = runTrelloApi(trello)
			if len(trelloInfos) > 0:
				trello_title = ""
				trello_info = ""
				for trelloInfo in trelloInfos:
					if "Access Denied" not in trelloInfo[0]:
						trello_title = "**Trello Boards Result**"
						trello_info = '* {0} - {1}\n'.format(trelloInfo[0], trelloInfo[1])
						sleep(2) # to prevent rate limting from URLScan.io
				report.write(trello_title)
				report.write(trello_info)
		if len(prezi) > 0:
			prezi_title = ""
			prezi_info = ""
			#report.write("\n**Prezi Info**\n")
			for preziInfo in prezi:
				page_title = getWebsiteTitle(preziInfo).strip()
				if "Page not found" not in page_title:
					prezi_title = "\n**Prezi Info**\n"
					prezi_info += '* {0} - {1}\n'.format(page_title, preziInfo)
					sleep(2) # to prevent rate limiting
			report.write(prezi_title)
			report.write(prezi_info)
		if len(codepen) > 0:
			codepen_title = ""
			codepen_info = ""
			for codepenInfo in codepen:
				page_title = getWebsiteTitle(codepenInfo).strip()
				if "404 Error" not in page_title:
					codepen_title = "\n**CodePen.io Pens**\n"
					codepen_info += '* {0} - {1}\n'.format(page_title, codepenInfo)
			report.write(codepen_title)
			report.write(codepen_info)

		if len(bookmarks) > 0:
			report.write("\n**Employee Personal Bookmarks**\n")
			for bookmarkInfo in bookmarks:
				page_title = getWebsiteTitle(bookmarkInfo).strip()
				report.write('* {0} - {1}\n'.format(page_title, bookmarkInfo))


main(sys.argv[1])
