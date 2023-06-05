import pandas as pd
from tabulate import tabulate
left_side = {}
right_side = {}
first = {}
follow = {}
RHS = []
rules = []
predict_set = []
non_terminals = set()
starting_non_terminal = None
terminals = set()
parse_table = {}
"""priority is just a map which shows the order of non-terminals that are going to be printed in parse table it does
   not have any implementation use """
priority = {}
welcome = """Hello!! this is LL(1) parser speaking, in order to parse your grammar you need to observe some rules :
1) In order to show the result of a production rule use -> .
2) Non-terminals should be uppercase letters,
   And terminals should be lowercase or other combinations of symbols (except -> and $ and | and micro).
3) Epsilon can be represented by "" . 
4) The first non-terminal of the first production rule will be assumed as the starting non-terminal.
5) Insert space after tokens you type and obviously type each production rule in a single line .
6) If you're done typing the grammar don't panic, just simply type done in the next line .
7) If your grammar was not LL(1) you will be informed.
8) DO NOT USE "" UNLESS FOR NULL PRODUCTION RULES LIKE D -> "" . 
An example of a valid grammar : 
E -> E + E | E * E
E -> id
done

Ok so you now know the rules and you even saw a valid example, that was it. READY? SET, GO! :"""

rule_index = 0

update = True


def extract_grammar(string):
    global rule_index
    global starting_non_terminal
    split = string.split()
    rhs_i = []
    last_l = 2
    non_terminal = split[0]
    if non_terminal.islower():
        print(f"You were supposed to enter uppercase letter as non-terminal :/")
        exit(0)
    if rule_index == 0:
        starting_non_terminal = non_terminal
    non_terminals.add(non_terminal)
    priority[non_terminal] = rule_index
    rules_i = [non_terminal, "->"]
    for i in range(2, len(split)):
        if split[i].isupper():
            rhs_i.insert(0, split[i])
            rules_i.append(split[i])
            non_terminals.add(split[i])
            if split[i] in right_side:
                right_side[split[i]].add((rule_index, i - last_l))
            else:
                right_side[split[i]] = {(rule_index, i - last_l)}
        elif split[i].islower():
            if split[i] == "micro":
                print(f"I said don't use micro as a terminal :/ don't believe me? then what is this:\n{split}")
                exit(0)
            if i - last_l != 0:
                rhs_i.insert(0, "micro")
                rhs_i.insert(0, split[i])
            else:
                rhs_i.insert(0, split[i])
            terminals.add(split[i])
            rules_i.append(split[i])
        elif split[i] == "|":
            if i - last_l == 0:
                print(f"One of your grammars were wrong : \n{split}\nWhy did you use | at the start of your rule ??:/")
                exit(0)
            else:
                RHS.append(rhs_i)
                rules.append(rules_i)
                if non_terminal in left_side:
                    left_side[non_terminal].add(rule_index)
                else:
                    left_side[non_terminal] = {rule_index}
                rules_i = [non_terminal, "->"]
                rhs_i = []
                rule_index = rule_index + 1
                last_l = i + 1
        elif split[i] == "->":
            print(f"I said don't use -> as a terminal :/ don't believe me? then what is this:\n{split}")
            exit(0)
        elif split[i] == "$":
            print(f"I said don't use $ as a terminal :/ don't believe me? then what is this:\n{split}")
            exit(0)
        else:
            if i - last_l != 0:
                rhs_i.insert(0, "micro")
                rhs_i.insert(0, split[i])
            else:
                if split[i] != '""':
                    rhs_i.insert(0, split[i])
            if split[i] != '""':
                terminals.add(split[i])
            rules_i.append(split[i])
    RHS.append(rhs_i)
    rules.append(rules_i)
    if non_terminal in left_side:
        left_side[non_terminal].add(rule_index)
    else:
        left_side[non_terminal] = {rule_index}
    rule_index = rule_index + 1


def update_first(non_terminal):
    global update
    before = first[non_terminal].copy()
    for l_pos in left_side[non_terminal]:
        if rules[l_pos][2] in terminals or rules[l_pos][2] == '""':
            first[non_terminal].add(rules[l_pos][2])
        else:
            for i in range(2, len(rules[l_pos])):
                u_set = first[rules[l_pos][i]].copy()
                if '""' in u_set:
                    if i != len(rules[l_pos]) - 1:
                        u_set.remove('""')
                    first[non_terminal].update(u_set)
                else:
                    first[non_terminal].update(u_set)
                    break
    if before != first[non_terminal]:
        update = True


def update_follow(non_terminal):
    global update
    before = follow[non_terminal].copy()
    if non_terminal not in right_side:
        return
    for r_pos in right_side[non_terminal]:
        rule = rules[r_pos[0]]
        if r_pos[1] + 2 == len(rule) - 1:
            follow[non_terminal].update(follow[rule[0]])
        else:
            for i in range(r_pos[1] + 3, len(rule)):
                if rule[i] in terminals:
                    follow[non_terminal].add(rule[i])
                    break
                u_set = first[rule[i]].copy()
                if '""' in u_set:
                    u_set.remove('""')
                    follow[non_terminal].update(u_set)
                    if i == len(rule) - 1:
                        follow[non_terminal].update(follow[rule[0]])
                else:
                    follow[non_terminal].update(u_set)
                    break
    if before != follow[non_terminal]:
        update = True


def is_useless(non_terminal):
    if non_terminal not in left_side:
        return True
    if (non_terminal not in right_side) and T != starting_non_terminal:
        return True
    for i in left_side[T]:
        if T not in RHS[i]:
            return False
    return True


def predict(index):
    rule = rules[index]
    index_predict_set = set()
    for i in range(2, len(rule)):
        if rule[i] in terminals:
            index_predict_set.add(rule[i])
            break
        if rule[i] == '""':
            index_predict_set.update(follow[rule[0]])
            break
        u_set = first[rule[i]].copy()
        if '""' in first[rule[i]]:
            u_set.remove('""')
            index_predict_set.update(u_set)
            if i == len(rule) - 1:
                index_predict_set.update(follow[rule[0]])
        else:
            index_predict_set.update(u_set)
            break
    predict_set.insert(index, index_predict_set)


def construct_parse_table():
    is_ll1 = True
    for nt in non_terminals:
        parse_table[nt] = {}

    for t in terminals:
        for nt in non_terminals:
            for i in left_side[nt]:
                if t in predict_set[i]:
                    if t in parse_table[nt]:
                        is_ll1 = False
                    else:
                        parse_table[nt][t] = []
                    parse_table[nt][t].append(i)
            if t not in parse_table[nt]:
                parse_table[nt][t] = [-1]
    return is_ll1


print(welcome)
comm = input()

while comm != "done":
    extract_grammar(comm)
    comm = input()

for T in non_terminals:
    first[T] = set()
    follow[T] = set()

follow[starting_non_terminal].add("$")

for T in non_terminals:
    if is_useless(T):
        print(f"""You have a useless non-terminal ({T}), that doesn't mean that your grammar is not LL(1) but it's 
better to enter a grammar with all non-terminals being, useful so I'll quite processing your grammar :)""")
        exit(0)
while update:
    update = False
    for T in non_terminals:
        update_first(T)
update = True
while update:
    update = False
    for T in non_terminals:
        update_follow(T)
for j in range(len(rules)):
    predict(j)
terminals.add("$")
ll1 = construct_parse_table()
terminals.remove("$")
terminals_list = list(terminals)
"just want to put the '$' at the end of the list which going to be printed in parse table"
terminals_list.append("$")
non_terminals_list = list(non_terminals)
"now we should sort the non-terminals-list in for parse table"
for j in range(len(non_terminals_list)):
    min_p = priority[non_terminals_list[j]]
    min_i = j
    for k in range(j + 1, len(non_terminals_list)):
        if priority[non_terminals_list[k]] < min_p:
            min_p = priority[non_terminals_list[k]]
            min_i = k
    temp = non_terminals_list[j]
    non_terminals_list[j] = non_terminals_list[min_i]
    non_terminals_list[min_i] = temp
"this section creates data frame of nullable , first, and follow for each non-terminal"
f_f_n_for_show = {"nullable": [],
                  "first": [],
                  "follow": []}
for ntr in non_terminals_list:
    if '""' in first[ntr]:
        f_f_n_for_show["nullable"].append("Y")
    else:
        f_f_n_for_show["nullable"].append("N")
    f_f_n_for_show["first"].append(' '.join(first[ntr]))
    f_f_n_for_show["follow"].append(' '.join(follow[ntr]))
f_f_n_for_show["nullable"] = pd.Series(f_f_n_for_show["nullable"], index=non_terminals_list)
f_f_n_for_show["first"] = pd.Series(f_f_n_for_show["first"], index=non_terminals_list)
f_f_n_for_show["follow"] = pd.Series(f_f_n_for_show["follow"], index=non_terminals_list)

f_f_n_df = pd.DataFrame(f_f_n_for_show)
"this section creates data frame of rules and RHS"
rules_for_show = {"Production Rules": pd.Series(' '.join(e) for e in rules)}
RHS_for_show = {"RHS": pd.Series(' '.join(e) for e in RHS)}

rules_df = pd.DataFrame(rules_for_show)
RHS_df = pd.DataFrame(RHS_for_show)

"this section creates data frame of parse table"
parse_table_for_show = {}
for tr in terminals_list:
    data = []
    for ntr in non_terminals_list:
        data.append(' '.join(str(e) for e in parse_table[ntr][tr]))
    parse_table_for_show[tr] = pd.Series(data, index=non_terminals_list)

parse_table_df = pd.DataFrame(parse_table_for_show)


"""this section is the print section, first the rules will be printed then the nullable ,first ,follow table after 
that parse table will be printed and at last RHS """
print(f"{tabulate(rules_df, headers='keys', tablefmt='fancy_grid')}\n")
print(f"""nullable/first/follow table:

{tabulate(f_f_n_df, headers='keys', tablefmt='fancy_grid')}\n""")
print(f"""And this is the parse table:

{tabulate(parse_table_df, headers='keys', tablefmt='fancy_grid')}\n""")
print(f"{tabulate(RHS_df, headers='keys', tablefmt='fancy_grid')}\n")
if not ll1:
    print("GRAMMAR IS NOT LL(1)\n")
print("""Now you can enter a string for me to parse, After entering the string the parse stack will be printed 
after each step and then you should enter one of tree letters(r/n/e) r means restart which restarts the 
process, n will show you the next step and e will terminate the process.""")
while True:
    Error = False
    finished = False
    string_to_parse = input("Enter the string (don't forget to put space between):\n")
    string_to_parse = string_to_parse.split()
    string_to_parse.append("$")
    stack = ['$', starting_non_terminal]
    parse_stack = [["parse stack"], [' '.join(stack)]]
    remaining_string = [["remaining string"], [' '.join(string_to_parse)]]
    current_rule = [["rule"], []]
    print(tabulate(parse_stack, headers='firstrow', tablefmt='fancy_grid'))
    print(tabulate(remaining_string, headers='firstrow', tablefmt='fancy_grid'))
    print(tabulate(current_rule, headers='firstrow', tablefmt='fancy_grid'))
    pointer = 0
    while True:
        comm = input("command : ")
        if comm == 'r':
            break
        if comm == 'e':
            print("See you later")
            exit(0)
        top = stack[-1]
        if top in terminals:
            pointer = pointer + 1
            stack.pop()
            parse_stack[1] = [' '.join(stack)]
            remaining_string[1] = [' '.join(string_to_parse[s] for s in range(pointer, len(string_to_parse)))]
            current_rule[1] = [f"matching {top}"]
        elif top in non_terminals:
            if string_to_parse[pointer] in terminals or string_to_parse[pointer] == "$":
                parse_pointer = parse_table[top][string_to_parse[pointer]][0]
                stack.pop()
                if parse_pointer != -1:
                    stack.extend(RHS[parse_pointer])
                    parse_stack[1] = [' '.join(stack)]
                    current_rule[1] = [' '.join(rules[parse_pointer])]
                else:
                    Error = True
                    current_rule[1] = [f"There is no rule which can lead non-terminal {top} to terminal {string_to_parse[pointer]} (string not accepted)"]
            else:
                Error = True
                current_rule[1] = [f"Word {string_to_parse[pointer]} is not a terminal (string not accepted)"]
        elif top == "micro":
            stack.pop()
            if stack[-1] != string_to_parse[pointer]:
                Error = True
                current_rule[1] = [f"Expected {stack[-1]}, got {string_to_parse[pointer]} instead (string not accepted)"]
            else:
                pointer = pointer+1
                match = stack.pop()
                parse_stack[1] = [' '.join(stack)]
                remaining_string[1] = [' '.join(string_to_parse[s] for s in range(pointer, len(string_to_parse)))]
                current_rule[1] = [f"matching {match}"]
        elif top == "$":
            if top == string_to_parse[pointer]:
                pointer = pointer + 1
                stack.pop()
                parse_stack[1] = [' '.join(stack)]
                remaining_string[1] = [' '.join(string_to_parse[s] for s in range(pointer, len(string_to_parse)))]
                current_rule[1] = [f"finished parsing (string accepted)"]
                finished = True
            else:
                Error = True
                current_rule[1] = [f"Expected {top}, got {string_to_parse[pointer]} instead (string not accepted)"]
        if Error:
            finished = True
        print(tabulate(parse_stack, headers='firstrow', tablefmt='fancy_grid'))
        print(tabulate(remaining_string, headers='firstrow', tablefmt='fancy_grid'))
        print(tabulate(current_rule, headers='firstrow', tablefmt='fancy_grid'))
        if finished:
            break
