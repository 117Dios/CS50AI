import os
import random
import re
import sys
import copy

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
    print(f"PageRank Results from Iteration")  # noqa: F541
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
    
    model = dict()
    
    n = len(corpus)
    
    links = corpus[page]
    
    for file in corpus:
        if links:
            if file in links:
                model[file] = (1-damping_factor)/n + damping_factor/len(links)
            else:
                model[file] = (1-damping_factor)/n
        else:
            model[file] = 1/n
    
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    samples = dict()
    
    for page in corpus:
        samples[page] = 0
    
    page = random.choice(list(corpus.keys()))
    
    for _ in range(n):
        
        samples[page] += 1
        
        model = transition_model(corpus=corpus,page=page,damping_factor=damping_factor)

        model_keys = list(model.keys())
        model_values = list(model.values())
        
        page = random.choices(model_keys,weights=model_values,k=1)[0]

    normalized_samples = samples.copy()
    
    for sample in samples:
        normalized_samples[sample] /= n
        
    return normalized_samples


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
   
    iterative_rank = dict()
   
    n = len(corpus)
    
    converge_value = 0.001
    actual_difference = 1
    
    for file in corpus:
        iterative_rank[file] = 1/n
    
    temp_rank = copy.deepcopy(iterative_rank)
    
    while actual_difference >= converge_value:
        for page1 in corpus:       
            page1_probability = (1 - damping_factor) / n  
            for page2 in corpus:       
                if page1 in corpus[page2]:
                    page1_probability += damping_factor * iterative_rank[page2]/len(corpus[page2])
                if not corpus[page2]:
                    page1_probability += damping_factor * iterative_rank[page2]/n

            temp_rank[page1] = page1_probability
        
    
        actual_difference = max(abs(iterative_rank[p] - temp_rank[p]) for p in iterative_rank)
        
        iterative_rank = copy.deepcopy(temp_rank)

    return temp_rank


if __name__ == "__main__":
    main()
