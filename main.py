import httplib2
import csv
from bs4 import BeautifulSoup, SoupStrainer


# class of nodes. I keep the from link and every link that exists inside the from link
class Node:

    def __init__(self, node_id, node_link, category):
        self.to_link = set()
        self.node_link = node_link
        self.category = category
        self.node_id = node_id

    def add_link(self, url):
        if self.node_link != url:
            self.to_link.add(url)


# we need to check the slashes in order to distinguish the recipe links from the general category links
def check_slashes(hrefs):
    slash_counter = 0
    for element in hrefs:
        if element == '/':
            slash_counter += 1
    if slash_counter <= 6:
        return False
    return True

#return id of node to_link
def node_id_from_link(link):
  for node in all_nodes:
      if link==node.node_link:
          return node.node_id
  return -1

all_nodes = []  # all the nodes
already_searched = []  # keep in track the links that we have already examined so we only examine each link only once
search_list = []  # keep in track the links we need to examine
base_html = "https://akispetretzikis.com/"  # the links inside the website is stored without the beginning of the url
http = httplib2.Http()
# the link from which we begin
html_string = 'https://akispetretzikis.com/el/categories/glyka/paradosiako-mwsaiko'
search_list.append(html_string)
html_string = 'https://akispetretzikis.com/el/categories/pswmia-zymes/chwriatiko-pswmi'
search_list.append(html_string)
html_string = 'https://akispetretzikis.com/el/categories/zymarika/makaronia-me-kima'
search_list.append(html_string)
html_string = 'https://akispetretzikis.com/el/categories/almyres-pites-tartes/chwriatikh-kotopita'
search_list.append(html_string)

# while we have links to examine
counter = 0
while search_list:
    current_http = search_list.pop()
    # if we already have examined a link we do not need to examine it twice
    if current_http in already_searched:
        continue
    counter +=1
    # create a node for every url we want to examine
    node = Node(counter,current_http, current_http.split('/')[-2])
    # get the links of the recipes recommended from the current_http
    response = http.request(current_http, 'GET')[1].decode()
    soup = BeautifulSoup(response, features="html.parser")
    div = soup.find('div', id='cmeProductSlatePaginiationTop')
    section = soup.find('section')
    # some link's don't have recommended sections
    if section is not None:
        # for every link inside the recommended section
        for a in section.find_all('a', href=True):
            # add the base_html and check slashed
            link = base_html + a['href']
            if check_slashes(link):
                node.add_link(link)  # add the link to the current url
                search_list.append(link)  # add that link to the search list
        all_nodes.append(node)  # after we add the links we add the node to our list of all the nodes

    # after we have successfully examined the url we add it to the already_searched list in order for the program to
    # know which urls we have examined
    already_searched.append(current_http)

# list which we will write to the csv file with the categories
row_list_nodes = [["Id", "Category", "Label"]]
counter = 0
for n in all_nodes:  # for every node
    from_link = n.node_link
    row_list_nodes.append(
        [n.node_id, n.category, from_link.split('/')[-1]])

# write the row_list to a csv file called gephi_categories.csv
with open('gephi_categories.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(row_list_nodes)

# list which we will write to the csv file for the relations
row_list_edges = [["Source", "Target"]]
counter = 0
for n in all_nodes:  # for every node
    from_link = n.node_link
    for to_link_url in n.to_link:  # for every link from that comes from every url we have examined
        id_from_link = node_id_from_link(to_link_url)
        if id_from_link!=-1:
            row_list_edges.append(
                [n.node_id, id_from_link])

        ##row_list_edges.append(
         ##   [n.node_id, node_id_from_link(to_link_url.split('/')[-1])])

# write the row_list to a csv file called gephi_relations.csv
with open('gephi_relations.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(row_list_edges)


print("Done writing the csv file")


