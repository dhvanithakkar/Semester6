EPSILON = "ε"
DOLLAR = "$"

def ignore_epsilon(elements: list[str]) -> list[str]:
    return [element for element in elements if element != EPSILON]

def is_terminal(element: str) -> bool:
    return element.islower() or element == EPSILON or element == DOLLAR or element in "()+*/!|"

def is_variable(element: str) -> bool:
    return element.isupper()

def has_epsilon(first_list: list[str]) -> bool:
    return EPSILON in first_list

def first_of_rule(rule: str, grammar) -> list[str]:
    first_list = []
    elem_first_list = []

    for element in rule:
        if is_terminal(element):
            first_list.append(element)
            break
        
        elif is_variable(element):
            elem_first_list = first(grammar, element)
            first_list.extend(ignore_epsilon(elem_first_list))

            if not has_epsilon(elem_first_list):
                break
    
    if rule and has_epsilon(elem_first_list):
        first_list.append(EPSILON)
    return first_list

def first(grammar, variable):
    first_list = []

    for rule in grammar[variable]:
        first_list.extend(first_of_rule(rule, grammar))
    
    return sorted(list(set(first_list)))

def all_firsts(grammar):
    firsts = {}
    for variable in grammar.keys():
        firsts[variable] = first(grammar, variable)
    return firsts

def in_RHS(variable: str, grammar) -> bool:
    for RHS in grammar.values():
        for rule in RHS:
            if variable in rule:
                return True
    return False

def get_parts_after_variable(rule, variable):
    parts = []
    start = 0
    while (index := rule.find(variable, start)) != -1:
        parts.append(rule[index + len(variable):])
        start = index + 1
    return parts

def follow(variable, grammar, start_variable):
    follow_list = []
    if variable == start_variable:
        follow_list.append(DOLLAR)

        if not in_RHS(variable, grammar):
            return follow_list
    
    for LHS in grammar:
        for rule in grammar[LHS]:
            parts = get_parts_after_variable(rule, variable)
            for part in parts:
                if not part:
                    if LHS != variable:
                        follow_list.extend(follow(LHS, grammar, start_variable))
                else:
                    first_part = first_of_rule(part, grammar)
                    follow_list.extend(ignore_epsilon(first_part))
                    if has_epsilon(first_part):
                        if LHS != variable:
                            follow_list.extend(follow(LHS, grammar, start_variable))
    return sorted(list(set(follow_list)))

def all_follows(grammar, start_variable):
    follows = {}
    for variable in grammar.keys():
        follows[variable] = follow(variable, grammar, start_variable)
    return follows

def eliminate_left_recursion(grammar):
    new_grammar = {}
    variables = list(grammar.keys())
    for var in variables:
        productions = grammar[var]
        left_rules = []
        non_left_rules = []
        for prod in productions:
            if prod.startswith(var):
                left_rules.append(prod[len(var):])
            else:
                non_left_rules.append(prod)
        if left_rules:
            new_var = var + "'"
            new_productions = [prod + new_var for prod in non_left_rules]
            new_grammar[var] = new_productions
            new_grammar[new_var] = [prod + new_var for prod in left_rules] + [EPSILON]
        else:
            new_grammar[var] = productions
    return new_grammar

def build_parsing_table(grammar, firsts, follows):
    parsing_table = {}
    for variable in grammar:
        parsing_table[variable] = {}
        for production in grammar[variable]:
            first_alpha = first_of_rule(production, grammar)
            for terminal in first_alpha:
                if terminal != EPSILON:
                    if terminal in parsing_table[variable]:
                        raise Exception(f"Conflict at {variable}, {terminal}: multiple productions")
                    parsing_table[variable][terminal] = production
            if EPSILON in first_alpha:
                for terminal in follows[variable]:
                    if terminal in parsing_table[variable]:
                        if parsing_table[variable][terminal] != production:
                            raise Exception(f"Conflict at {variable}, {terminal} (epsilon case)")
                    parsing_table[variable][terminal] = production
                if DOLLAR in follows[variable]:
                    if DOLLAR in parsing_table[variable]:
                        if parsing_table[variable][DOLLAR] != production:
                            raise Exception(f"Conflict at {variable}, $ (epsilon case)")
                    parsing_table[variable][DOLLAR] = production
    return parsing_table

# Example usage:
start_variable = "E"
original_grammar = {
    "E": ["E+T", "T"], 
    "T": ["T*F", "F"],
    "F": ["(E)", "i"]
}

# Eliminate left recursion
modified_grammar = eliminate_left_recursion(original_grammar)
print("Modified Grammar after Left Recursion Elimination:")
for var in modified_grammar:
    print(f"{var} -> {' | '.join(modified_grammar[var])}")

# Compute First and Follow sets
firsts = all_firsts(modified_grammar)
follows = all_follows(modified_grammar, start_variable)

print("\nFirst sets:")
for var, first_set in firsts.items():
    print(f"First({var}) = {first_set}")

print("\nFollow sets:")
for var, follow_set in follows.items():
    print(f"Follow({var}) = {follow_set}")

# Build parsing table
try:
    parsing_table = build_parsing_table(modified_grammar, firsts, follows)
    print("\nPredictive Parsing Table:")
    for var in parsing_table:
        print(f"{var}:")
        for terminal in parsing_table[var]:
            print(f"  {terminal}: {parsing_table[var][terminal]}")
except Exception as e:
    print(f"\nError building parsing table: {e}")
