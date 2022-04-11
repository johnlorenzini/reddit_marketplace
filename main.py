from time import sleep
from pync import Notifier
import praw, os

f = open('ids_found.txt', 'a')
valid = {'a': 'appleswap', 'h': 'hardwareswap', 'm': 'mechmarket', 'o': 'mousemarket'}

def prompt(message):
    return input(message)
    
def subreddits():
    sel = ''
    while True:
        _clear()
        nxt = prompt(f'--------------------------------\nreddit marketplace:\nselect/remove subreddits\n--------------------------------\na: appleswap\nh: hardwareswap\nm: mechmarket\no: mousemarket\n\nselected: "{", ".join(sorted(valid[item] for item in list(sel)))}"\n--------------------------------\npress ENTER to continue\n--------------------------------\n').strip().lower()
        _clear()
        if nxt not in valid.keys():
            if len(nxt) == 0:
                if len(sel) == 0:
                    print('no subreddits selected\ntry again')
                else:
                    break
            else: 
                print(f'invalid selection "{nxt}"')
            sleep(1)     
        else: 
            if nxt in sel:
                print(f'removed "{valid[nxt]}"') 
                sel = sel.replace(nxt, "")
            else: 
                print(f'selected "{valid[nxt]}"')
                sel += nxt
        sleep(.5)
    _clear()
    return sorted(valid[item] for item in list(sel))

def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_search():
    _clear()
    return prompt(f"--------------------------------\nenter a specific search\nor press ENTER to skip\n--------------------------------\n")

def get_price():
    _clear()
    price = prompt(f"--------------------------------\nenter a maximum budget\nor press ENTER to skip\n--------------------------------\n$")
    if len(price) > 0:
        try: return float(price)
        except:
            _clear()
            print('invalid price, skipping')
            sleep(1)
    else:
        return None

def run():
    simulate(subreddits(), praw.Reddit('MP', user_agent="marketplace_scanner"), get_search(), get_price())

def simulate(srs, client, search, price):
    _clear()
    cont = prompt(f"--------------------------------\nsummary:\n\nsubreddits: {str(srs)[1:-1]}\nsearch: {search}\nprice: ${price}\n--------------------------------\ncontinue? (y/n)\n")
    _clear()
    if cont == 'y':
        while True:
            f = open('ids_found.txt', 'r+')
            tags = f.readlines()
            for sr in srs:
                match = []
                for post in client.subreddit(sr).new(limit=200):
                    if str(post.id) + "\n" not in tags:
                        if search.lower() in str(post.title).lower():
                            match.append(post)
                        f.write(post.id + "\n")
                print_search(sr, match)
            f.close()
            sleep(5)
            _clear()
            for i in range(59, -1, -1):
                print(f'--------------------------------\nfinished, sleeping for\n{i} second(s)\n--------------------------------\n')
                sleep(1)
                _clear()

def print_search(sr, posts):
    if len(posts) > 0:
        print(f'{len(posts)} new results found in subreddit {sr}:\n--------------------------------\n')
        for post in posts:
            try:
                title = post.title[post.title.index('[H]'):]
            except:
                title = post.title
            url = str(post.url)
            print(f'title: {title}\nurl: {url}\n\n')
            Notifier.notify('new listing found', title=sr, open=url)
        print('\n--------------------------------\n')
    else:
        print(f'\n--------------------------------\nfound no new results in subreddit {sr}\n--------------------------------\n')

        


if __name__ == '__main__':
    run()
