from itertools import chain, combinations


class AssociationRules:


    def __init__(self, itemsets):
        self.itemsets = itemsets # List containing all the itemsets obtained by the previous stage
                                 # e.g. in self.itemsets[0] there will be a dictionary with keys the itemsets and as values the support for each itemset
        
        self.flat_itemsets = {}

        for itemset_dict in itemsets:
            for itemset, support in itemset_dict.items():
                self.flat_itemsets[itemset] = support

        self.association_rules = None


    def powerset(self, input_iterable):
        "powerset([1,2,3]) --> (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(input_iterable)
        return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1)))

        
    # Util method that flattens a list given in input
    def flat_list(self, input_list):
        # Flattening the list
        flat_list = []
        for sublist in input_list:
            for item in sublist:
                flat_list.append(item)

        # Removing eventual duplicates
        flat_list = list(set(flat_list))

        return flat_list
    

    # This method is useful to get the same itemset notation that we find in the main dictionary, 
    # This will be used when the support of a certain itemset is needed
    # Returns a ordered tuple, as the keys of the dictionary
    def order_itemset(self, itemset):        
        itemset_list = list(itemset)

        if len(itemset_list) == 1:
            return itemset_list[0]

        itemset_list = sorted(itemset_list)
        return tuple(itemset_list)


    # Given one single itemset as input, the function generates all the possible association rules in form of list of sets
    # The itemset given as input is a set itself
    # In the first set we have the antecedent, in the second set we have the consequence
    # [set(antecedent), set(consequence)]
    def generate_association_rules(self, frequent_itemset, itemset_support):
        rules = []

        subsets = self.powerset(frequent_itemset)

        for subset in subsets:
            antecedent = set(subset)
            consequence = frequent_itemset.difference(antecedent)

            rules.append([antecedent, consequence])

        return rules


    # Main idea here, if I find one association rule that is below confidence I can skip all the others that have less literals in the antecedent.
    # In position 2 of the list that represents the rule we store the confidence of such rule.
    def filter_association_rules(self, association_rules_list, confidence_threshold):
        filtered_rules = []

        for rule in association_rules_list:
            confidence = self.compute_confidence(rule)
            if self.compute_confidence(rule) > confidence_threshold:
                filtered_rules.append(rule.append(confidence))

        return filtered_rules


    # Compute the confidence level of the given association rule as list
    # The list has two items, the first is a set of the items composing the antecedent and the second item is a set of items of the consequence
    # The confidence is computed by the ratio: support of the union of the antecedent and sequent and the support of the antecedent alone 
    def compute_confidence(self, association_rule):
        confidence = 0.0

        union = association_rule[0].union(association_rule[1])

        union_support = self.flat_itemsets[self.order_itemset(union)]
        antecedent_support = self.flat_itemsets[self.order_itemset(association_rule[0])]

        confidence = union_support / antecedent_support

        return confidence


    # Entry point of the class.
    # After the instantiation of the object, this method computes all the association rules from the itemsets
    # considering the threshold in order to filter them
    def generate_all_rules(self, confidence_threshold):
        self.association_rules = []
        
        for i, itemset_group in enumerate(self.itemsets):
            if i == 0:
                continue # skipping the single-item itemsets (the cannot generate any rule!          

            else:
                print("Computing the itemsets with ", i + 1, " elements")
                for itemset, support in itemset_group.items():
                    association_rules = self.generate_association_rules(set(itemset), support)
                    filtered_rules = self.filter_association_rules(association_rules, confidence_threshold)
                    self.association_rules.append(filtered_rules)

        self.association_rules = self.flat_list(self.association_rules)

        return self.association_rules

