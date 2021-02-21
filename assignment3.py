import argparse
import urllib.request
import re
import csv
import datetime



def downloadData(url):
    """Pull Down Web Log File"""
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    return csv.reader(lines)


def processData(data):
    """Processes the data from the CSV"""
    lines = 0
    pictures = 0
    browsers = {'firefox': 0, 'Chrome': 0, 'IE': 0, 'Safari': 0}

    #Create a dictionary of 24 hours, Extra credit
    hours = {}
    for i in range(0,25): hours[i] = 0

    #Process the data by row
    for row in data:
        lines = lines + 1
        """Search for Image Hits"""
        if(re.match(r".*(.jpg|.gif|.png)$", row[0], re.IGNORECASE)):
            pictures = pictures + 1
        index = datetime.datetime.strptime(row[1], "%Y-%m-%d  %H:%M:%S")
        hours[index.hour] += 1

        """Count each time a browser is user
        Firefox = FireFox
        AppleWebsite = Safari
        Look for chromeframe first to determine if it is a Chrome Browser
        Since some MSIE entries also contain chromeframe"""
        if (re.search(r".*firefox", row[2], re.IGNORECASE)):
            browsers['firefox'] += 1
            continue
        if (re.search(r".*appleWebkit", row[2], re.IGNORECASE)):
            browsers['Safari'] += 1
            continue
        if (re.search(r".*chromeframe", row[2], re.IGNORECASE)):
            browsers['Chrome'] += 1
            continue
        if (re.search(r".*msie", row[2], re.IGNORECASE)):
            browsers['IE'] += 1
            continue

    #Determine how many images account for the request
    print(f"Image requests account for {(pictures / lines) * 100}% of all requests")

    #Determine the most popular bowser, the item in the dictionary with the highest number
    popbrowser = sorted(browsers.items(), key = lambda kv:(kv[1]))
    print(f"The browser that is most popular is:  {popbrowser[-1][0]} with {popbrowser[-1][1]} uses")

    #Extra Credit - list of hours sorted by total number of hits in that hour
    sortedhits = sorted(hours.items(), key=lambda kv: (kv[1]))
    for i in reversed(sortedhits):
        print(f"hour {i[0]} has {i[1]} hits")

def main(url):
    print(f"Running main with URL = {url}...")
    processData(downloadData(url))

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)










