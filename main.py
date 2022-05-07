headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

pages = ['https://www.amazon.in/s?k=mixer&rh=n%3A4375446031&ref=nb_sb_noss'] 
pages_10 = [str('https://www.amazon.in/s?k=mixer&i=kitchen&rh=n%3A4375446031&page=2&qid=1651850965&ref=sr_pg_' + str(i)) for i in range(2, 11)]

pagesn = pages + pages_10
links = []


for page in pagesn:
    one_page = requests.get(page, headers = headers)
    print(one_page.status_code)
    sp = bs4.BeautifulSoup(one_page.content, 'html.parser')
    links_only = sp.select('a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')
    for i in range(len(links_only)):
        if i % 2 == 0:
            links.append('https://www.amazon.in/'+links_only[i]['href'])



count = 1
reviews = []
for link in links:
    f = np.random.random() * 10
    time.sleep(f)
    print(f'{count} done with {f} seconds')
    page = requests.get(link, headers = headers)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    # names.append(soup.find('span', id = 'productTitle').text)
    rev = soup.find('span', id = 'acrCustomerReviewText')
    name = soup.find('span', id = 'productTitle')
    if name != None:
        name = name.text.rstrip().lstrip()
    else:
        name = None
    price = soup.select('span.a-offscreen')
    if len(price) > 0:
        p = float(re.sub('[^0-9.]', '', price[0].text))
    else:
        p = None
    if rev != None:
        reviews.append([count, name, float(re.sub('[^0-9]', '', rev.text)), p])
    elif rev == None:
        reviews.append([count, name, None, p])
    if (name != None) and (count != None) and (rev != None) and (p != None):
        print(name, rev, p)
    
    count += 1

df = pd.DataFrame(reviews, columns = ['Count', 'Name', 'Ratings', 'Price'])
print(df)
