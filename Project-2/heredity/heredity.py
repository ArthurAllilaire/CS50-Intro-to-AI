import csv
import itertools
import sys
import math

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def dict_of_gene_and_trait(people_set, one_gene, two_genes, have_trait):
    """
    Takes a set of people then returns Dictionary matching a person to a tuple
    # (num_genes, trait (0 or 1))
    """
    need_to_calc = {}

    for person in one_gene:
        # By default people are calculated for not expressing the trait
        need_to_calc[person] = (1, 0)

    for person in two_genes:
        # By default people are calculated for not expressing the trait
        need_to_calc[person] = (2, 0)

    # Get the rest of the people
    for person in people_set.difference(one_gene, two_genes):
        need_to_calc[person] = (0, 0)

    for person in have_trait:
        # Get tuple
        tup = need_to_calc[person]
        # Change to be calculating for the person
        need_to_calc[person] = (tup[0], 1)

    return need_to_calc


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    probs = []
    # Dictionary matching a person to a tuple
    # (num_genes, trait (0 or 1))

    to_calc = dict_of_gene_and_trait(
        set(people.keys()), one_gene, two_genes, have_trait)

    for person in people:
        # Calculate chance of having or not having gene
        # num_genes = to_calc[person][0]
        prob_gene = prob_has_gene(people, person, to_calc)
        # Calculate chance of having trait, given that she has or doesn't have the gene
        # Use PROBS dict, example query: PROBS["trait"][1][False]
        prob_trait = PROBS["trait"][to_calc[person]
                                    [0]][bool(to_calc[person][1])]
        # Append the multiplication of both probabilties.
        probs.append(prob_gene * prob_trait)

    # Multiply all the probabilities together and
    # Return the joint probability
    return math.prod(probs)


def prob_has_gene(people, person, genes_and_traits):
    """
    Takes a person and the num of genes that is being predicted.
    Returns the probability the person has that gene
    """
    # Dictionary of values for current person (name, mother, father, trait)
    profile = people[person]
    num_genes = genes_and_traits[person][0]
    # Check if person has no parents
    if profile["mother"] == None and profile["father"] == None:
        # If they don't Use probability constants in PROBS dict to get probability.

        return PROBS["gene"][num_genes]

    # Get the genes of parents
    parents = (genes_and_traits[profile["mother"]]
               [0], genes_and_traits[profile["father"]][0])

    # Probability distributation defining probability a parent passes on 1 gene, [0] = 0 genes, [1] if parent has 1 gene. 1- prob dist is probability parent passes on no genes.
    prob_dist_parents = [PROBS["mutation"], 0.5, 1-PROBS["mutation"]]

    # Prob of mum who has parents[0] genes passing on 1 gene
    prob_mum_1 = prob_dist_parents[parents[0]]
    # and prob of dad who has parent[1] genes passin on 0 genes
    prob_dad_1 = prob_dist_parents[parents[1]]

    prob_dist_child = [
        # The probability of getting 0 genes is equal to
        # Prob of mum passing on 0 genes
        # and prob of dad passin on 0 genes
        # Since it is AND multiply together.
        (1-prob_mum_1) * (1-prob_dad_1),


        # The probability of getting 1 gene is equal to 1- prob(0) + 1-prob(2)
        # Placeholder for now
        0,

        # The probability of getting 2 genes is equal to
        # probability of dad and mum passing on 1 gene each
        # Since it is AND multiply together.
        prob_dad_1 * prob_mum_1
    ]
    # Add probability of 1
    # The probability of getting 1 gene is equal to 1- prob(0) + 1-prob(2)
    prob_dist_child[1] = 1 - sum(prob_dist_child)

    return prob_dist_child[num_genes]


def prob_has_trait(people, ):
    pass


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
