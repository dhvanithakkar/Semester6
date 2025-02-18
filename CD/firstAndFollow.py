"""

X → ABC
A→a∣ε
B→b∣ε
C→c∣d

"""

EPSILON = "ε"
DOLLAR = "$"

def ignore_epsilon(elements: list[str]) -> list[str]:
    return [element for element in elements if element != EPSILON]

def is_terminal(element: str) -> bool:
    return element.islower() or element == EPSILON

def is_variable(element: str) -> bool:
    return element.isupper()

def has_epsilon(first_list: list[str]) -> bool:
    return EPSILON in first_list

def first_of_rule(rule: str) -> list[str]:
    first_list = []
    elem_first_list = []

    for element in rule:
        if is_terminal(element):
            # Includes simple epsilon rule.
            # Epsilon can only explicitly be mentioned as -> EPSILON and that is caught here.
            first_list.append(element)
            break
        
        elif is_variable(element):
            elem_first_list = first(grammar, element)
            # Should not give epsilon here midway.
            # It only shows up if the rule elements were over with epsilon present
            first_list.extend(ignore_epsilon(elem_first_list))

            if not has_epsilon(elem_first_list):
                # So it does not have to go further in the rule. First was found.
                break
    
    # If by the last element in the rule there is an epsilon, add that to First.
    if has_epsilon(elem_first_list):
        first_list.append(EPSILON)
    return first_list


def first(grammar, variable):
    first_list = []

    for rule in grammar[variable]:
        first_list.extend(first_of_rule(rule))
    
    return sorted(list(set(first_list)))

def all_firsts(grammar):
    firsts = {}
    for variable in grammar.keys():
        firsts[variable]= first(grammar, variable)
    
    return firsts


def all_follows(grammar, start_variable):
    follows = {}
    for variable in grammar.keys():
        follows[variable] = follow(variable, grammar, start_variable)
    
    return follows

# start_variable = "X"
# grammar = {"X": ["ABC"], "A": ["a", EPSILON], "B": ["b", EPSILON], "C": ["c", "d"]}
# print(first(grammar, start_variable))


# 
# 
# 
# 

def in_RHS(variable: str, grammar) -> bool:
    for RHS in grammar.values():
        if variable in RHS:
            return True
    return False


# Cache follow here.
def follow(variable, grammar, start_variable):
    follow_list = []
    print(variable, ": ")
    if variable == start_variable:
        follow_list.append(DOLLAR)

        # Ayaan does not like this condition. RHS dekh hi raha anyway. Fair.
        if not in_RHS(variable, grammar):
            print("NOT IN RHS, dollar only", follow_list)
            return follow_list
        
    # "A": ["BC", "EFGH", "H"]
    for LHS, RHS in grammar.items():
        for rule in RHS:
            if variable in rule:
                print("RULE FOUND:", LHS, "->", rule)
                parts = rule.split(variable)
                
                
                if parts[-1] == "":
                    print("END OF RULE, FOLLOW PARENT:", LHS)
                    follow_list.extend(follow(LHS, grammar, start_variable))
                
                else:                    
                    # new_rule is a substring of the rule string where it is: FIRST OCCURENCE OF VARIABLE -> END
                    # new_rule = "".join(parts[1:])
                    first_occurence = rule.find(variable)
                    new_rule =  rule[first_occurence + 1:]

                    f = first_of_rule(new_rule)
                    print("FIRST OF:", new_rule, "IS", f)

                    if has_epsilon(f):
                        print("EPSILON IN FIRST OF", new_rule, ": FOLLOWS :", LHS)
                        follow_list.extend(follow(LHS, grammar, start_variable))
                        f = ignore_epsilon(f)
                    follow_list.extend(f)
    
    follow_list = sorted(list(set(follow_list)))
    print("FOLLOW OF:", variable, follow_list)
    return follow_list

start_variable = "A"
grammar = {"A": ["BC", "EFGH", "H"], "B": ["b"], "C": ["c", EPSILON], "E": ["e", EPSILON], "F": ["CE"], "G": ["g"], "H": ["h", EPSILON]}

# start_variable = 'S'
# grammar = {'S':['ACB', 'CbB', 'Ba'], 'B':['g', EPSILON], 'A' : ['da', 'BC'], 'C': ['h', EPSILON]}


# print(first(grammar, start_variable))
print(all_firsts(grammar))
print(all_follows(grammar, start_variable))
