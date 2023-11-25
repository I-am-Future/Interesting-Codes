def match(pattern, test_string):
    # Initialize the index variables
    pattern_idx = 0
    string_idx = 0
    star_idx = -1
    star_match = 0
    
    # While there are still characters to match
    while string_idx < len(test_string):
        # If the current characters match or the pattern has a "?"
        if pattern_idx < len(pattern) and (pattern[pattern_idx] == test_string[string_idx] or pattern[pattern_idx] == "?"):
            pattern_idx += 1
            string_idx += 1
        # If the pattern has a "*"
        elif pattern_idx < len(pattern) and pattern[pattern_idx] == "*":
            star_idx = pattern_idx
            star_match = string_idx
            pattern_idx += 1
        # If the pattern had a "*" before and the current character matches
        elif star_idx != -1:
            pattern_idx = star_idx + 1
            star_match += 1
            string_idx = star_match
        # If none of the above conditions are met, the string doesn't match
        else:
            return False
        
    # If there are still characters in the pattern that aren't "*", the string doesn't match
    while pattern_idx < len(pattern) and pattern[pattern_idx] == "*":
        pattern_idx += 1
        
    return pattern_idx == len(pattern)




# Test cases with "?" symbol
assert match("h?llo", "hello") == True
assert match("h?llo", "hallo") == True
assert match("h?llo", "hhllo") == True
assert match("h?llo", "hllo") == False
assert match("h?llo", "heeeo") == False

# Test cases with "*" symbol
assert match("h*llo", "hello") == True
assert match("h*llo", "hllo") == True
assert match("h*llo", "heeeello") == True
assert match("h*llo", "hxllo") == True
assert match("h*llo", "hi there") == False
assert match("h**llo", "hello") == True

# Test cases with combinations of "?" and "*" symbols
assert match("h?llo*", "hello") == True
assert match("h?llo*", "hallo") == True
assert match("h?llo*", "hhlloooo") == True
assert match("h?llo*", "hllooo") == False
assert match("h?llo*", "heeeo") == False

# Test cases with special characters and spaces
assert match("*u*p", "i love python programming") == False
assert match("*u*p", "up") == True
assert match("bu?n??s ai??s", "buenos días") == False
assert match("bu?n??s ai??s", "buenos dias") == False
assert match("bu?n??s ai??s", "buenas tardes") == False
assert match("*j?vasc?ipt", "javascript is cool") == False
assert match("*j?vasc?ipt", "jvascipt") == False
