import os
import random
import re
import sys


DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    numPages = len(corpus)
    numLinks = len(corpus[page])

    if numLinks == 0 :
        return dict([(pages,1/numPages) for pages in corpus])

    probabilityDistribution =  dict([(pages,(1-damping_factor)/numPages) for pages in corpus])
    for linkPage in corpus[page]:
        probabilityDistribution[linkPage] += damping_factor/numLinks

    return probabilityDistribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    appear = dict([(page,0) for page in corpus])
    numPages = len(corpus)
    
    probabilites = dict([(page,1/numPages) for page in corpus])
    sample = random.choices(list(probabilites.keys()), weights=probabilites.values(), k=1)
    appear[sample[0]] +=1
    
    for _ in range(1,n):
        probabilites = transition_model(corpus,sample[0],damping_factor)
        sample = random.choices(list(probabilites.keys()), weights=probabilites.values(), k=1)
        appear[sample[0]] +=1
    

    return dict([(key,value/n) for key,value in appear.items()])

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    numPages = len(corpus)

    probabilities = dict([(page,1/numPages) for page in corpus])

    while True:
        newprobabilities = dict([(page,computeProba(corpus,page,probabilities,damping_factor)) for page in corpus])

        difference = [newprobabilities[page]-probabilities[page] for page in probabilities]

        if all(abs(i) <= 0.001 for i in difference):
            break

        probabilities = newprobabilities

    return probabilities

def computeProba(corpus,page,probabilities,damping_factor):
    
    numPages = len(corpus)

    proba = (1-damping_factor)/numPages

    for possiblePage in corpus:
        if page in corpus[possiblePage]:
            numLinks = len(corpus[possiblePage])
            proba += damping_factor/numLinks*probabilities[possiblePage]
        elif len(possiblePage) == 0 :
            proba += 1/numPages

    return proba

if __name__ == "__main__":
    main()
