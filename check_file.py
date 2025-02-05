import sys
import os
import re

METHOD_MODIFIERS = ["public", "protected", "default", "private", "static", "abstract", "final", "synchronized", "native", "strictfp"]

ENTITIES_WITH_INTERNAL_JAVADOC = ["class", "interface", "record"]

def remove_package_and_imports(string):
    '''Return a string that is the input string with leading package declarations and import statements removed. This function assumes the package declarations and import statements are all at the start of `string`, excluding whitespace, so this function should only be called after comments have already been removed from `string`.'''
    return re.sub(r"^\s*(?:(?:package|import).*;\s*)+", "", string)

def remove_java_comments(string):
    '''Return a string that is the input string with all Java comments (excluding Javadoc) removed. This function only removes the comments themselves, not any whitespace (e.g., indents) immediately before the comment.'''
    new_string = ""
    first_idx_after_prev_comment = 0
    while True:
        # Find the next occurrances of "//" and "/*" (but not "/**" unless it's "/**/") outside of strings and javadoc blocks
        line_comment_idx = regex_search_ignoring_comments_and_literals(r'\/\/', string, first_idx_after_prev_comment)
        block_comment_idx = regex_search_ignoring_comments_and_literals(r'\/\*(?=[^*]|\*\/)', string, first_idx_after_prev_comment)
        if line_comment_idx == block_comment_idx == -1:
            new_string += string[first_idx_after_prev_comment:]
            break
        elif block_comment_idx == -1 or (line_comment_idx != -1 and line_comment_idx < block_comment_idx):
            comment_start_idx = line_comment_idx
            comment_end_idx = string.find("\n", comment_start_idx)
            comment_ender_len = 1
        else:
            comment_start_idx = block_comment_idx
            comment_end_idx = string.find("*/", comment_start_idx + 2)
            comment_ender_len = 2
        new_string += string[first_idx_after_prev_comment:comment_start_idx]
        if comment_end_idx == -1:
            # The comment includes the very last characters of the string
            break
        first_idx_after_prev_comment = comment_end_idx + comment_ender_len
    return new_string
            

def regex_search_ignoring_comments_and_literals(regex, string, start_idx=0):
    '''Return the index of the first match for `regex` within `string` starting no earlier than `start_idx`, excluding occurrances inside Java comments, string literals, and character literals (assuming `string` does not start already in the midst of one of those).'''
    in_block_comment = False
    in_line_comment = False
    in_string = False
    in_char = False
    escape = False
    # How char_iter is about to be constructed:
    # Calling enumerate produces a pairing of indices and characters
    # Calling list makes it subscriptable, which enables...
    # The slicing post-enumeration keeps the integrity of the indices, rather than causing them to start at 0
    # Calling iter allows us to call next within the loop to skip the next character
    char_iter = iter(list(enumerate(string))[start_idx:])
    for curr_idx, curr_char in char_iter:
        if escape:
            escape = False
            continue
        if re.match(regex, string[curr_idx:]) and not any([in_block_comment, in_line_comment, in_string, in_char]):
            return curr_idx
        if curr_idx < len(string) - 1:
            next_char = string[curr_idx + 1]
            if (in_string or in_char) and curr_char == '\\':
                escape = True
            if curr_char == '/' and next_char == '*' and not any([in_line_comment, in_string]):
                in_block_comment = True
                # Skip the next character since we know it's an asterisk
                next(char_iter)
            if curr_char == '*' and next_char == '/':
                in_block_comment = False
                # Skip the next character since we know it's a slash
                next(char_iter)
            if curr_char == '/' and next_char == '/' and not any([in_block_comment, in_string]):
                in_line_comment = True
                # Skip the next character since we know it's a slash
                next(char_iter)
            if curr_char == '\n':
                in_line_comment = False
            if curr_char == '"' and not any([in_block_comment, in_line_comment, in_char]):
                in_string = not in_string
            if curr_char == "'" and not any([in_block_comment, in_line_comment, in_string]):
                in_char = not in_char
    return -1

def split_excluding_enclosed(string, split_char, opening_char, closing_char):
    '''Return a list of strings resulting from splitting `string` around instances of `split_char`, except for instances of `split_char` that occur while there have been any `opening_char`s encountered that are unmatched by `closing_char`s. No instances, of any of the above, inside comments or literals are counted. This function assumes that all instances of `opening_char` are properly matched with a `closing_char` instance in `string`.'''
    
    # Initialize an empty list to store the substrings
    substrings = []
    # Beginning index of the substring about to be added
    start_of_curr_substring = 0
    # Index after most recent match or split_char instance found
    search_start_idx = 0

    while True:

        # Find the next split_char or opening_char, if any
        found_idx = regex_search_ignoring_comments_and_literals(f"{re.escape(split_char)}|{re.escape(opening_char)}", string, search_start_idx)
        if found_idx == -1:
            # No more split_char instances, so append the final substring and return the list
            substrings.append(string[start_of_curr_substring:])
            return substrings
        
        # If it's an instance of split_char, add the most recent substring to the list
        if string[found_idx] == split_char:
            substrings.append(string[start_of_curr_substring:found_idx])

            # Jump to after this instance
            start_of_curr_substring = search_start_idx = found_idx + 1

        # Otherwise, prepare to search again from after the closing_char that matches this opening char, while keeping the same starting point for the current substring
        else:
            search_start_idx = get_idx_after_matching_char(string, found_idx, closing_char) + 1


def parse_method_sig(sig):
    '''Given a string representation of a valid Java method signature, return a tuple containing the following values:
     - A boolean that is True iff the function has a non-void return type (and is not a constructor)
     - A string containing the method's name and parameter types
     - A list of the names of the parameters of the method
     - A list of the types of the exceptions this method throws
     - A string that is either "method" or "constructor" representing which one was parsed'''

    # Get rid of method modifier keywords
    words = sig.split()
    while words[0] in METHOD_MODIFIERS:
        del words[0]
    sig = " ".join(words)

    # 1. Determine the method name (or class name, if this is a constructor)
    
    # Slice the signature to include only the portion before its parameters,
    # and find the last non-empty substring (minus its trailing whitespace) that follows a "]", ">", or whitespace character therein
    pre_paren_split_around_closers = re.split(r"[\]>\s]", sig[ : sig.index("(")])
    while len(pre_paren_split_around_closers[-1]) == 0:
        del pre_paren_split_around_closers[-1]
    method_name = pre_paren_split_around_closers[-1]

    # 2. Determine if "@return" documentation is needed

    # Determine if this is a constructor signature
    is_constructor = len(pre_paren_split_around_closers) == 1

    # Determine if "@return" is needed
    # words[0] might not be the full return type if it is an array or generic type, but all we need to know is whether or not it's void
    needs_return_doc = words[0] != "void" and not is_constructor

    # 3. Parse all the parameter types and names

    # Slice the signature to include only the parameters portion
    params_substr = sig[sig.index("(")+1 : sig.index(")")].strip()

    # Check if there are any parameters at all
    if len(params_substr):

        # Split the parameters portion of the signature into substrings each containing one parameter (i.e., one type-name pair each)
        # Can't just use the Python split function because there might be misleading commas if any of the types are generics
        params = split_excluding_enclosed(params_substr, ",", "<", ">")

        # For each parameter, parse its type (that is, all but the last "word" separated by '>'|']'|' ' of the parameter) and eliminate any spaces therein, and parse its name (that is, the last "word" of the parameter)
        param_types = []
        param_names = []
        for param in params:
            param = param.strip()
            possible_word_enders = list(re.finditer(r">|\]|\s", param)) # There should be at least one of these in order for the file to have compiled
            name_idx = possible_word_enders[-1].end()
            param_types.append(re.sub("\s", "", param[:name_idx]))
            param_names.append(param[name_idx:])
    
    # If there aren't any parameters, produce empty lists
    else:
        param_types = []
        param_names = []
    
    # 4. Produce a string representation unique to this signature (according to Java rules)
    method_name_and_params = f"{method_name}({', '.join(param_types)})"

    # 5. Parse all of the exception types that can be thrown (if any)
    throws_idx = sig.find("throws ", sig.index(")"))
    if throws_idx != -1:
        exception_types = [exception.strip() for exception in sig[throws_idx + 7 : ].split(",")]
    else:
        exception_types = []

    # Ready to return a big tuple!
    return needs_return_doc, method_name_and_params, param_names, exception_types, "constructor" if is_constructor else "method"

def get_idx_after_matching_char(string, opener_idx, closing_char):
    '''Return the index of the character in `string` that follows the closing character (specified by `closing_char`) that matches the opening character at `opener_idx`. This function assumes that there is indeed a closing character to match the opening character at `string[opener_idx]`.'''
    
    # Determine the opening character
    opening_char = string[opener_idx]

    # Initialize these booleans that all need to be false for brackets to count
    in_block_comment = False
    in_line_comment = False
    in_string = False
    in_char = False
    escape = False

    # Loop until num_open is 0
    num_open = 1
    curr_idx = opener_idx + 1
    while True:

        # Skip this character if the previous one was a backslash 
        if escape:
            curr_idx += 1
            escape = False
            continue

        # Update the current character
        curr_char = string[curr_idx]

        # Update the unmatched open bracket count, if this character is a bracket and actually counts
        num_open += curr_char == opening_char and not any([in_block_comment, in_line_comment, in_string, in_char])
        num_open -= curr_char == closing_char and not any([in_block_comment, in_line_comment, in_string, in_char])
        
        # Check if the match has been found
        if num_open == 0:
            break

        # Update the next character
        next_char = string[curr_idx + 1]

        # Check if we've entered or exited a comment or a literal
        if (in_string or in_char) and curr_char == '\\':
            escape = True
        if curr_char == '/' and next_char == '*' and not any([in_line_comment, in_string]):
            in_block_comment = True
            # Skip the next character since we know it's an asterisk
            curr_idx += 1
        if curr_char == '*' and next_char == '/':
            in_block_comment = False
            # Skip the next character since we know it's a slash
            curr_idx += 1
        if curr_char == '/' and next_char == '/' and not any([in_block_comment, in_string]):
            in_line_comment = True
            # Skip the next character since we know it's a slash
            curr_idx += 1
        if curr_char == '\n':
            in_line_comment = False
        if curr_char == '"' and not any([in_block_comment, in_line_comment, in_char]):
            in_string = not in_string
        if curr_char == "'" and not any([in_block_comment, in_line_comment, in_string]):
            in_char = not in_char

        # Move on to the next character
        curr_idx += 1
    
    # Return the index of the matching closing bracket
    return curr_idx + 1

def remove_upcoming_annotations(string, start_idx):
    '''Return the input `string` with "upcoming" annotations removed. "Upcoming" annotations are those that occur after position `start_idx` in `string` and before the next non-annotation, non-Javadoc code.'''

    # Define a pattern that will match 0 or more Javadoc blocks (capturing them) followed by an at symbol and annotation name (need to confirm it's not "interface" since this is a valid way follow an at symbol but not as an annotation we want to remove)
    javadoc_and_annotation_name_pattern = re.compile(r"(\s*(?:/\*\*.*\*/\s*)*)@\s*(?!interface)[\w\$\.]*\s*", flags=re.S)

    # See if there is even a single annotation
    annotation_match = javadoc_and_annotation_name_pattern.match(string, start_idx)
    while annotation_match:

        # Remove a matching paren group if one follows the annotation name
        possible_paren_idx = annotation_match.end()
        if string[possible_paren_idx] == '(':
            string = string[:possible_paren_idx] + string[get_idx_after_matching_char(string, possible_paren_idx, ')'):]

        # Remove the at symbol, annotation name, and trailing whitespace; leave everything else (including any Javadoc, which is preserved in capturing group #1)
        string = string[:start_idx] + javadoc_and_annotation_name_pattern.sub(r"\1", string[start_idx:], 1)

        # Check for another annotation here
        annotation_match = javadoc_and_annotation_name_pattern.match(string, start_idx)
    
    return string

def check_entity_body(entity_text, problems, entity_type, entity_name):
    '''Check `entity_text` (which should be exactly the body of a Java class/interface/etc.--whichever one is given in `entity_type`--excluding the curly brackets surrounding the body) for any Javadoc issues, and append descriptive messages for those issues to `problems`.'''

    chars_read = 0
    while True:

        # Remove any annotations we are about to encounter
        entity_text = remove_upcoming_annotations(entity_text, chars_read)
            
        # Confirm that there's another method, class/interface/etc., or attribute (without checking which one yet)
        open_bracket_idx = regex_search_ignoring_comments_and_literals('\\{', entity_text, chars_read)
        semicolon_idx = regex_search_ignoring_comments_and_literals('\\;', entity_text, chars_read)
        if -1 == semicolon_idx == open_bracket_idx:
            # All methods/classes/interfaces/attributes/etc. inside this class have been addressed
            break

        # Check if the next method/class/interface/attribute/etc. is either a concrete method or a class/interface/etc. declaration
        if open_bracket_idx != -1 and (semicolon_idx == -1 or open_bracket_idx < semicolon_idx):
            # We found a '{'
            
            # Check if we found a nested class/interface/etc.
            idx_before_keyword = regex_search_ignoring_comments_and_literals(r"\s(?:class|@?interface|enum|record)\s", entity_text[:open_bracket_idx], chars_read)
            if idx_before_keyword != -1:

                # We found a nested class/interface/etc., so recursively check it
                nested_entity_type = re.match(r"class|@?interface|enum|record", entity_text[idx_before_keyword + 1 : ])[0]
                idx_after_entity_closer = get_idx_after_matching_char(entity_text, open_bracket_idx, '}')
                check_entity(entity_text[chars_read:idx_after_entity_closer], problems, nested_entity_type, entity_name)
                
                # Now, move ahead to after the end of the nested entity and continue from there
                chars_read = get_idx_after_matching_char(entity_text, open_bracket_idx, '}')
                continue

            # Check if this is an attribute assignment involving an array literal
            if '=' in entity_text[chars_read:open_bracket_idx]:
                # It is an assignment, so move on to after the matching closing bracket and try again (there'll probably be a semicolon that will be handled in the next iteration)
                chars_read = get_idx_after_matching_char(entity_text, open_bracket_idx, '}')
                continue
            # Okay, it's a normal method
            is_abstract_method = False
        else:
            # Need to determine if this is an attribute declaration/assignment or an abstract method declaration
            if '(' in entity_text[chars_read:semicolon_idx] and '=' not in entity_text[chars_read:semicolon_idx]:
                is_abstract_method = True
            else:
                # This semicolon was just part of an attribute declaration/assignment, so move on to the following character and try again
                chars_read = semicolon_idx + 1
                continue
        
        # Okay, at this point we've determined that we're looking at a method.
        # Use the appropriate post-method-signature index depending on whether the method was determined to be abstract or concrete
        idx_after_sig = semicolon_idx if is_abstract_method else open_bracket_idx
        
        # Attempt to separate this method's docstring and signature
        docstring_and_sig = entity_text[chars_read : idx_after_sig] # Includes all immediately previous whitespace characters, including newlines
        try:
            docstring, sig = re.split('\\s*\\*\\/\\s*', docstring_and_sig)
            missing_method_javadoc = False
        except ValueError: # there is no occurrance of "*/" in docstring_and_sig, so there are not enough values to unpack
            # No javadoc found for this method
            missing_method_javadoc = True
            sig = docstring_and_sig.strip()

        # Parse the method's signature
        needs_return_tag, method_name, param_names, exception_types, method_or_constructor = parse_method_sig(sig)

        # If this method contains no javadoc whatsoever, complain once and skip it
        if missing_method_javadoc:
            problems.append(f"Missing javadoc or forgotten javadoc symbol (\"/**\") for {method_or_constructor} \"{method_name}\" in {entity_type} \"{entity_name}\"")
            # Update the reading offset to be after this method
            if is_abstract_method:
                chars_read = idx_after_sig + 1
            else:
                chars_read = get_idx_after_matching_char(entity_text, idx_after_sig, '}')
            continue

        # Parse the docstring
        docstring_parts = re.split(r'\s*\n\s*\*?\s*@(?=(?:param)|(?:return)|(?:throws)|(?:exception))', docstring)        
        
        # Validate method summary
        try:
            method_descr = docstring_parts[0][docstring_parts[0].index('/**')+3 : ]
        except ValueError:
            # This shouldn't happen now that all non-javadoc comments were removed from the file text, but just in case...
            problems.append(f"Forgotten Javadoc symbol (\"/**\") before method \"{method_name}\"")
            method_descr = docstring_parts[0][docstring_parts[0].index('/*')+2 : ]
        if re.match("^[\\*\\s]*$", method_descr):
                problems.append(f"Missing method summary for {method_or_constructor} \"{method_name}\" in {entity_type} \"{entity_name}\"")

        # Note all param, return, and throws/exception tags that are present and have a description after them; complain about any that shouldn't be here
        for part in docstring_parts[1:]:
            words = part.split()
            if words[0] == "param":
                if len(words) > 1:
                    if words[1] in param_names:
                        if len(words) > 2:
                            param_names.remove(words[1])
                    else:
                        problems.append(f"Unexpected \"@param {words[1]}\" documentation for {method_or_constructor} \"{method_name}\" in {entity_type} \"{entity_name}\"")
                else:
                    problems.append(f"Unfinished \"@param\" documentation before {method_or_constructor} \"{method_name}\" in {entity_type} \"{entity_name}\"")
            elif words[0] == "return":
                if needs_return_tag:
                    if len(words) > 1:
                        needs_return_tag = False
                else:
                    problems.append(f"Unexpected \"@return\" documentation for {method_or_constructor} \"{method_name}\" in {entity_type} \"{entity_name}\"")
            elif words[0] in ["throws", "exception"]:
                if len(words) > 1:
                    if words[1] in exception_types:
                        if len(words) > 2:
                            exception_types.remove(words[1])
                    elif len(words) < 3:
                        # We'll allow any exception to be documented, even if it isn't in the signature, as long as it has a description. Since this one doesn't have one, complain
                        problems.append(f"Unfinished \"@{words[0]} {words[1]}\" documentation for {method_or_constructor} \"{method_name}\" in {entity_type} \"{entity_name}\"")
                else:
                    problems.append(f"Unfinished \"@{words[0]}\" documentation before {method_or_constructor} \"{method_name}\" in {entity_type} \"{entity_name}\"")
        
        # Add any missing param, return, and throws/exception tags to the list of problems
        for param in param_names:
            problems.append(f"Missing \"@param {param}\" documentation for {method_or_constructor} \"{method_name}\" in {entity_type} \"{entity_name}\"")
        if needs_return_tag:
            problems.append(f"Missing \"@return\" documentation for {method_or_constructor} \"{method_name}\" in {entity_type} \"{entity_name}\"")
        for exception in exception_types:
            problems.append(f"Missing \"@throws {exception}\" documentation for {method_or_constructor} \"{method_name}\" in {entity_type} \"{entity_name}\"")

        # Update the reading offset to be after this method
        if is_abstract_method:
            chars_read = idx_after_sig + 1
        else:
            chars_read = get_idx_after_matching_char(entity_text, idx_after_sig, '}')

def check_entity(text, problems, entity_type, enclosing_names=""):
    '''Check the external and internal javadoc for the sole class/interface/etc. (specified in `entity_type`) contained in `text`. Append any problems encountered to `problems`.'''

    # Determine the printable entity type
    printable_entity_type = "annotation" if entity_type == "@interface" else entity_type

    # Determine the entity name (including dots if this is a nested entity)
    keyword_idx = regex_search_ignoring_comments_and_literals(entity_type, text)
    entity_name = re.match(entity_type + r"\s+([\w\$]+)", text[keyword_idx:])[1]
    if enclosing_names:
        entity_name = enclosing_names + "." + entity_name

    # Confirm that the entity declaration has any javadoc block at all, that it is not empty, and that it doesn't contain method-specific tags
    pre_entity_substr = text[:keyword_idx] # Includes any "public"/"abstract"/"final" before the entity, as well as any javadoc)
    try:
        comment_end_idx = pre_entity_substr.index('*/')
        try:
            entity_descr = pre_entity_substr[pre_entity_substr.index('/**')+3 : comment_end_idx]
        except ValueError:
            # This shouldn't happen now that all non-javadoc comments were removed from the file text, but just in case...
            problems.append(f"Forgotten javadoc symbol (\"/**\") before {printable_entity_type} declaration for {printable_entity_type} \"{entity_name}\"")
            entity_descr = pre_entity_substr[pre_entity_substr.index('/*')+2 : comment_end_idx]
        if re.match(r"[\*\s]*$", entity_descr):
            problems.append(f"Missing {printable_entity_type} summary before {printable_entity_type} \"{entity_name}\"")
        # See if the javadoc contains a method-specific tag
        for tag in ["@return", "@throws", "@exception"]:
            if re.search(f"\\n\\s*\\*?\\s*{tag}", entity_descr):
                problems.append(f"Method-specific tag \"{tag}\" found in {printable_entity_type} summary before {printable_entity_type} \"{entity_name}\"")
        # See if the javadoc begins with a tag (aside from the method-specific tags)
        initial_tag_match = re.match(r"[\*\s]*(@(?!param|return|throws|exception)\w+)", entity_descr)
        if initial_tag_match:
            problems.append(f"Missing {printable_entity_type} summary before {printable_entity_type} \"{entity_name}\" (needs to be before \"{initial_tag_match[1]}\" tag)")
    except ValueError:
        problems.append(f"Missing javadoc or forgotten javadoc symbol (\"/**\") before {printable_entity_type} declaration for {printable_entity_type} \"{entity_name}\"")

    # Now, if the entity is one that should have javadoc inside, check the entity body: start checking after the entity opening curly bracket and go until (exclusive) the entity closing curly bracket
    if entity_type in ENTITIES_WITH_INTERNAL_JAVADOC:
        idx_after_entity_opener = regex_search_ignoring_comments_and_literals('\\{', text, keyword_idx) + 1
        idx_after_entity_closer = get_idx_after_matching_char(text, idx_after_entity_opener - 1, '}')
        check_entity_body(text[idx_after_entity_opener : idx_after_entity_closer - 1], problems, entity_type, entity_name)

def check_file(f):
    '''Check if all of the methods and classes/interfaces/records/enums/annotations in Java file `f` (a file object, not a file name) have appropriate javadoc--a summary in all cases, plus params, return, and/or throws for methods (as applicable for specific methods)--and return all of the javadoc insufficiencies discovered. This function assumes that the file compiles successfully.'''
    
    # Initialize the list of found javadoc problems
    problems = []

    # Read the file text into memory
    file_text = f.read()

    # Get rid of comments, so that there's only whitespace between javadoc and their classes/interfaces/methods/etc.
    file_text = remove_java_comments(file_text)

    # Get rid of any package declaration and import statements
    file_text = remove_package_and_imports(file_text)
    
    # Check each of the classes/etc. in the file
    idx_after_prev_entity_end = 0
    while True:

        # Remove any annotations we are about to encounter
        file_text = remove_upcoming_annotations(file_text, idx_after_prev_entity_end)

        # Locate the start of a class/interface/etc.; make sure we find the keyword not inside javadoc
        keyword_idx = regex_search_ignoring_comments_and_literals(r"class|@?interface|enum|record", file_text, idx_after_prev_entity_end)

        # Check if there are no more classes/etc. in the file
        if keyword_idx == -1:
            break
            
        # Determine the entity type
        entity_type = re.match(r"class|@?interface|enum|record", file_text[keyword_idx:])[0]
        
        # Check this entity
        idx_after_entity_opener = regex_search_ignoring_comments_and_literals('\\{', file_text, keyword_idx) + 1
        idx_after_entity_closer = get_idx_after_matching_char(file_text, idx_after_entity_opener - 1, '}')
        check_entity(file_text[idx_after_prev_entity_end:idx_after_entity_closer], problems, entity_type)
    
        # Prepare for next iteration
        idx_after_prev_entity_end = idx_after_entity_closer
    
    # Return the list of descriptions of missing javadoc aspects
    return problems

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {os.path.basename(__file__)} <FirstFileToCheck.java> [SecondFileToCheck.java ...]")
        exit(1)
    any_problems = False
    for java_filename in sys.argv[1:]:
        try:
            with open(java_filename) as f:
                problems = check_file(f)
            if problems:
                print(f"\n{java_filename}:")
                print("\n".join(problems))
                any_problems = True
        except FileNotFoundError:
            print(f"\nFile \"{java_filename}\" not found.")
            exit(1)
    if any_problems:
        exit(3)
