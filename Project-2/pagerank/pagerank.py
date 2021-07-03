import os
import random
import re
import sys
import math

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
    result = {}
    # Get all the page links from the current page
    page_links = corpus[page]
    num_pages = len(corpus.keys())
    # If page has links then:
    if page_links:
        # The extra probability for every page linked in the corpus is:
        # damping factor divided by the number of pages
        linked_prob = damping_factor/len(page_links)
        # Every page gets base prob of 1- damping_factor / len(corpus.keys())
        page_prob = (1-damping_factor) / num_pages

        for page in corpus:
            if page in page_links:
                # round to 5 decimal points
                result[page] = round(linked_prob + page_prob, 5)
            else:
                result[page] = round(page_prob, 5)

    # If no links to the page then
    else:
        # Each page is equally likely to be selected
        page_prob = 1/num_pages
        for page in corpus:
            result[page] = page_prob

    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initiate a dictionary that is filled with every page, with the value of each key = 0, counter for num times page visited.
    result = {}
    pages = list(corpus.keys())
    for page in pages:
        result[page] = 0

    # take the first page at random
    page = random.choice(pages)
    # Go through all the iterations
    for iter in range(n):
        # For the first iteration just take the random page
        if iter != 1:
            # Else get the page based on the transition model probability
            model = transition_model(corpus, page, damping_factor)
            rand_dec = random.random()
            total_prob = 0
            for page_itr in pages:
                # Add to the total_prob the probability of this page
                total_prob += model[page_itr]
                # Less than as float can never be 1 so to get 5% for 0.05 need less than as can be 0 randomly select based on probability the page
                if rand_dec < total_prob:
                    page = page_itr
                    break

        # Record that the current page was visited
        result[page] += 1

    # Divide by number of trials to make sum == 1
    for page in result:
        result[page] = round(result[page] / n, 8)
    return result


def get_pages_that_link(corpus, current_page):
    """
    Returns a set of tuples of all the pages that link to the current_page. Each tuple is: (page_name, num_links_on_the_page)
    If page has no links then returns a set as if it had a link to every page including itself.
    """
    links = set()
    pages = list(corpus.keys())
    # Go over every page and add it to the set of tuples if it links to the current page
    for page in pages:
        if current_page in corpus[page]:
            # Add the page that links to it and the num_links of the page
            links.add((page, len(corpus[page])))

    """ # If the number of links is zero
    if len(links) == 0:
        # Then change it to as if it had a link to every page
        for page in pages:
            # Add the page that links to it and the num_links of the page
            links.add((page, len(corpus[page]))) """

    return links


def pagerank_calc(corpus, old_pagerank, damping_factor):
    """ Calculates new pagerank based on corpus and old pagerank, returns the new pagerank """
    new_pagerank = {}
    pages = list(corpus.keys())
    pagerank_base_prob = (1-damping_factor)/len(pages)

    for page in pages:
        # Set of tuples of all the links that link to the current page
        # (page_name, num_links_on_the_page)
        links = get_pages_that_link(corpus, page)

        # Sum of the PR of all the links to that page
        pr_links = 0
        for link in links:
            # Sum of page rank / numlinks(i)
            pr_links += old_pagerank[link[0]] / link[1]

        # print(f"pr for {page} is: {pr_links}")
        # Divide by num_links * damping factor probability
        pr_for_page = damping_factor * pr_links

        # Add that to the new pagerank
        new_pagerank[page] = round(pagerank_base_prob + pr_for_page, 8)

    return new_pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    start_pagerank = {}
    pages = corpus.keys()
    # Set the beginning page probability to 1/Num pages
    for page in pages:
        start_pagerank[page] = 1/len(pages)

    while True:
        # Calculate the pagerank
        old_pagerank = pagerank_calc(corpus, start_pagerank, damping_factor)
        old_values = list(old_pagerank.values())

        start_pagerank = pagerank_calc(corpus, old_pagerank, damping_factor)
        start_values = list(start_pagerank.values())

        close = True
        # print(old_pagerank, start_pagerank)
        for i in range(len(old_values)):
            old_val = old_values[i]
            new_val = start_values[i]
            # If they are too far apart
            if abs(old_val-new_val) > 0.001:
                close = False
                # Only need one value to be too far apart
                break

        # If all values where close enough
        if close:
            return start_pagerank


if __name__ == "__main__":
    main()
