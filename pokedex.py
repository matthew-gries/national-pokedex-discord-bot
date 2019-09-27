#module imports
from lxml import html
import requests

#class to represent our pokemon data
class Pokedex():
    #constructor: params: String[][], String[][]
    def __init__(self):
        #get content from online pokedex
        page = requests.get('https://pokemondb.net/pokedex/all')
        tree = html.fromstring(page.content)
        
        pokemon = tree.xpath('//tr')
    
        #the headers for our columns
        headers = []
        headers = makeHeaders(pokemon)

        #this will be our table
        info = []
        info = makeTable(pokemon)

        #this will be our image urls
        images = []
        images = makeImageUrls(pokemon)

        self.headers = headers
        self.info = info
        self.images = images



#HtmlElement -> String[]
#get headers for every column
def makeHeaders(pokemon):
    
    headers = []
    
    for h in pokemon[0]:
        headers.append(h.text_content())

    return headers



#HtmlElement -> String[][]
#return a table of pokedex information 
def makeTable(pokemon):
    
    #this will be our internal table
    info = []

    #add 10 empty arrays to info (these will be our columns)
    for i in range(10):
        info.append([])

    #add pokemon to info
    for i in range(1, len(pokemon)):
        #start at first row after header
        pokerow = pokemon[i]

        #for every col in the info grid
        for j in range(10):
            info[j].append(pokerow[j].text_content())

    #format names
    for i in range(len(info[1])):
        #get a name
        name = info[1][i]
    
        #if a space is found in the name then it needs to be formatted 
        # (as long as it is not the pokemon Type: Null)
        if name.find(' ') != -1 and not name.find(':') != -1:
            info[1][i] = formatName(name)

    for i in range(len(info[2])):
        #get a type
        ptype = info[2][i]

        #if a capital letter that is not the first captial letter is found,
        #format the type
        for letter in ptype[1:]:
            if letter.isupper():
                info[2][i] = formatType(ptype)
                break

    return info



#HtmlElement -> String[]
#Get URLs of images from HTML code
def makeImageUrls(pokemon):

    images = []

    #for every element in the html body, minus the header
    for i in range(1, len(pokemon)):
        
        img = pokemon[i][0].find_class('infocard-cell-img')
        #convert and format the element info a url
        img = html.tostring(img[0])
        img = str(img)
        img = img[img.find('data-src='):]
        img = img[:img.find(' ')]
        img = img.replace('data-src=', '')
        img = img.replace('"', '')

        #add to list
        images.append(img)

    return images



# String -> String
# Formats a Pokemon name into <name>: <modifier> <name>
def formatName(name):

    index = -1
    
    #find the index of the first capital letter, other than the start of their name
    for i in range(1, len(name)):	
        if name[i].isupper():
            index = i
            break

    #check that an index was found
    if index == -1:
        print('Something went wrong formatting this pokemon\'s name')
        return name	
    #continue formatting name
    else:
        nameFirst = name[:index]
        nameSecond = name[index:]
        newName = nameFirst + ': ' + nameSecond
        return newName



#String -> String
#Formats pokemon types with more than one type
def formatType(ptype):

    index = -1

    #find the index of the first capital letter after the first letter
    for i in range(1, len(ptype)):
        if ptype[i].isupper():
            index = i
            break 

    #check that an index was found
    if index == -1:
        print('Something went wrong formatting this pokemon\'s type')
        return ptype
    #continue formatting name
    else:
        ptypeFirst = ptype[:index]
        ptypeSecond = ptype[index:]
        ptype = ptypeFirst + '/' + ptypeSecond
        return ptype





    
