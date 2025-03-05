from copy import deepcopy
import sys
import os

def parse_readme(readme_file):
    '''Take in a pointer to a readme file and return a dictionary representing the file tree laid out in the final section of the readme. In the returned dictionary, directories are represented as keys, containing their names, whose values are nested dictionaries, and files are represented as keys (containing their names) whose values are None.
    
    #### README format expectations:
    - The files section must begin with the exact line "Files:" and should be the final section of the README.
    - Every non-blank line in the files section must represent a regular file; directories will be merely implied in file paths.
    - Directories in file paths must be separated by single forward slashes.
    - A line describing a file must begin (without any whitespace beforehand) with the file path, which must immediately precede the three-character string " - " (which may itself precede a description of the file).
    - If a file description is too long for one line, it may be broken into multiple lines as long as each new line begins with an indentation of at least one space. This flexibility extends to file descriptions (the part after the " - ") only, not file paths.'''

    readme_dict = dict()
    reached_files_section = False
    for line in readme_file:

        # Check if we've reached the files section
        if line.strip() == "Files:":
            reached_files_section = True
            continue

        # Skip any lines before the files section and any blank lines
        if not reached_files_section or line.strip() == "": 
            continue

        # Okay, we're on a non-blank line in the files section. 
        # If it starts with a space, it is (by established convention for this function) just a continuation of the most recent file's description, so skip this line
        if line[0] == " ":
            continue
        
        # Now we can assume the start of the line contains a file path, and we can finally process it
        file_path = line.split(" - ", 1)[0]
        file_path = file_path.strip()
        dirs, file_name = os.path.split(file_path)
        # Loop into (and create as needed) nested dictionaries representing the directories in this file's path
        curr_dict = readme_dict
        if dirs:
            for dir_name in dirs.split("/"):
                if dir_name not in curr_dict:
                    curr_dict[dir_name] = dict()
                curr_dict = curr_dict[dir_name]
        # Add this filename as a key in the dictionary corresponding to its parent directory
        if(os.path.isdir(file_path)):
            curr_dict[file_name] = dict()
        else:
            curr_dict[file_name] = None

    return readme_dict

def dict_matches_dir(readme_dict, dir, path_from_root=""):
    '''Check recursively if the files in the dictionary `readme_dict` (which should emulate a file tree) correspond one-to-one onto the actual files within directory `dir`. Print any mismatches. Return True iff there are no mismatches. `path_to_root` should only be used in the recursive calls; it makes the printing cleaner by eliminating the relative/absolute path to the directory of the root call.'''
    
    readme_dict = deepcopy(readme_dict) # since we'll delete from the dict
    all_good = True
    
    # Loop through the files/dirs that are actually in this directory
    for child in os.listdir(dir):

        # Calculate some values describing this child
        full_child_path = os.path.join(dir, child)
        child_path_from_root = os.path.join(path_from_root, child)
        is_dir_on_disk = os.path.isdir(full_child_path)

        # If the child is in the dict:
        if child in readme_dict:
            is_dir_in_dict = type(readme_dict[child]) is dict

            # If the child is a directory and is supposed to be a directory, recur
            if is_dir_on_disk and is_dir_in_dict:
                # The recursive call needs to come before the `and` because we don't want a short-circuit to prevent it from running (might miss out on a full printout of all the problems)
                all_good = dict_matches_dir(readme_dict[child], full_child_path, child_path_from_root) and all_good
            
            # Handle cases where the child is a file in the dict and a directory on the disk or vice versa
            elif not is_dir_in_dict and is_dir_on_disk:
                all_good = False
                print(f"Expected \"{child_path_from_root}\" to be a file, but actually found a directory within the zip")
            elif is_dir_in_dict and not is_dir_on_disk:
                all_good = False
                print(f"Expected \"{child_path_from_root}\" to be a directory, but actually found a file within the zip")

            # Remove the child from the dict
            del readme_dict[child]
        
        # If the child is not in the dict (i.e., not in the README), complain. Do not recur, for brevity. 
        else:
            all_good = False
            print(f"Unexpected {'directory' if is_dir_on_disk else 'file'} \"{child_path_from_root}\" was found within the zip")

    # Complain about each file/dir still in the dict (they were in the README but not in the actual directory)
    for child in readme_dict:
        all_good = False
        child_path_from_root = os.path.join(path_from_root, child)
        print(f"Expected {'file' if readme_dict[child] is None else 'directory'} \"{child_path_from_root}\" is missing from the zip")
    
    return all_good

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: python3 {os.path.basename(__file__)} <readme_file_to_check> <dir_to_check>")
        sys.exit(1)

    readme_filename = sys.argv[1]
    try:
        with open(readme_filename) as readme_file:
            readme_dict = parse_readme(readme_file)
    except FileNotFoundError:
        print(f"Readme file \"{readme_filename}\" not found")
        sys.exit(1)

    dir_path = sys.argv[2]
    if not os.path.isdir(dir_path):
        print(f"\"{dir_path}\" is not a valid directory")
        sys.exit(1)

    if not dict_matches_dir(readme_dict, dir_path):
        
        sys.exit(3)