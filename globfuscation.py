#!/usr/bin/env python3

#python .\globfuscation.py "C:\\Windows\\System32\\calc.exe"

import os
import pathlib
import pprint
import re
import itertools
import glob

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("target")
args = parser.parse_args()


def test_if_env_matches(test, target):
    regex_string = rf'^{test.replace("?", ".").replace("*", ".*")}$'
    matches = []
    for key in os.environ.keys():
        match = re.search(regex_string, key)
        if match:
            matches.append(match.group())
    return len(matches) == 1 and target in matches


def test_if_glob_matches(test, start_path, target):
    global glob_cache
    matches = [p for p in glob_cache[start_path] if pathlib.Path(p).match(test)]
    return len(matches) == 1 and target in matches


def glob_mutate(subpath):
    for each_possibility  in itertools.product("?X", repeat=len(subpath)):
        new_mutation = list(each_possibility)
        for i, c in enumerate(each_possibility):
            if c == "X":
                new_mutation[i] = subpath[i]
        to_test = "".join(new_mutation)
        yield to_test


def star_replace(subpath_mutation):
    return re.sub(r"\?+", "*", subpath_mutation)


def path_parts(path_str):
    return tuple(piece.strip("\\") for piece in pathlib.Path(path_str).parts)

def main():
    global glob_cache, args

    # target = r"C:\\Windows\\System32\\calc.exe"
    target = args.target

    short_mode = True

    target_norm_str = os.path.normpath(target)
    target_path = pathlib.Path(target_norm_str)
    if not target_path.is_absolute():
        print("[!] Error, Absolute Path Required!")

    env_score = {}
    target_parts = path_parts(target_norm_str)

    for env_key, value_path in os.environ.items():
        if os.path.exists(value_path) and os.path.isdir(value_path):
            
            value_path_norm_str = os.path.normpath(value_path)
            value_parts = path_parts(value_path_norm_str)

            if len(value_parts) <= len(target_parts):
                for i, part in enumerate(value_parts):
                    if target_parts[i] == value_parts[i]:
                        if env_key not in env_score:
                            env_score[env_key] = 1
                        else:
                            env_score[env_key] += 1
                    else:
                        env_score[env_key] = 0
                        break
                        
        
    best_envs = []
    highest_score_env = max(env_score, key=env_score.get)
    highest_score_value = env_score[highest_score_env]
    best_envs = [key for key, value in env_score.items() if value == highest_score_value]

    starting_matches = []
    for env_key in best_envs:
        env_matches = []

        env = os.path.normpath(os.environ[env_key])
        env_parts = path_parts(env)

        left_over_parts = target_parts[len(env_parts) :]

        for to_test in glob_mutate(env_key):
            matches = test_if_env_matches(to_test, env_key)
            if matches:
                env_matches.append(to_test)
        
        starting_matches.append(env_matches)



    env = os.path.normpath(os.environ[best_envs[0]])
    env_parts = path_parts(env)
    left_over_parts = target_parts[len(env_parts) :]

    print("caching subdirectories...")
    glob_cache = {}
    for i, subpart in enumerate(left_over_parts):
        map_path = os.path.join(env, os.path.sep.join(left_over_parts[:i]))
        glob_value = os.path.join(map_path, '*')
        glob_cache[map_path] = glob.glob(glob_value)


    # Handle subdirectory parts...
    print(f"finding globfuscation options for '{target}'...")
    remaining_matches = []
    for i, each_part in enumerate(left_over_parts):

        remaining_part = os.path.sep.join(left_over_parts[:i])
        base_path = os.path.join(env, remaining_part)
        full_path = os.path.join(env, remaining_part, each_part)

        question_mark_mutations = []
        max_length = 0
        for each_question_mark_mutation in glob_mutate(each_part):
            question_mark_mutation_path = os.path.join(
                env, remaining_part, each_question_mark_mutation
            )
            
            if test_if_glob_matches(question_mark_mutation_path, base_path, full_path):
                question_mark_mutations.append(each_question_mark_mutation)


        star_mutation_matches = []
        max_length = 10000
        for each_mutation in question_mark_mutations:
            star_mutation = star_replace(each_mutation)

            star_mutation_path = os.path.join(env, remaining_part, star_mutation)

            if len(star_mutation) >= max_length:
                continue

            if star_mutation not in star_mutation_matches:
                matches = test_if_glob_matches(star_mutation_path, base_path, full_path)
                if matches:
                    if short_mode:
                        if max_length == 0:
                            max_length = len(star_mutation)

                    max_length = len(star_mutation)
                    star_mutation_matches.append(star_mutation)

        remaining_matches.append(question_mark_mutations + star_mutation_matches)

    
    all_mode = False

    shortest = 0
    all_options = []
    for env_starts in starting_matches:
        for start in env_starts:
            for every_option in itertools.product(*remaining_matches):
                new_option = f"$env:{start}{os.path.sep}{os.path.join(*every_option)}"
                if all_mode:
                    print(new_option)
                else:
                    if shortest == 0:
                        shortest = len(new_option)
                    if len(new_option) < shortest:
                        print(new_option)
                        shortest = len(new_option)

if __name__ == "__main__":
    main()
