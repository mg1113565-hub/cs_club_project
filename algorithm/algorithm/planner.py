import json
from pathlib import Path


def get_major_data(student, data):
    """Return (requirements, courses, warnings) for the program the student picked at each school."""
    # TODO: student["programs"] = {"sjsu": "cs", "ucb": "math"}. For each school/program and each college,
    #       agreement = data["agreements"].get((college, school, program)), missing -> warning "No data yet for lpc to UCB math".
    #       requirements = {"SJSU: CS 46B": [options from every college]}, courses = {id: course} for the student's colleges.


def requirement_done(options, completed):
    """Return True if every course in at least one option is completed."""
    # TODO: Loop through options; an option is done when all of its courses are in completed.


def pick_option(options, completed, needed, courses):
    """Return the option with the fewest units left; completed or needed courses count as 0, tie -> first."""
    # TODO: For each option add up the units of courses not in completed or needed, keep the smallest.


def find_needed_courses(requirements, completed, courses):
    """Return (needed, warnings) where needed = {course_id: [requirement labels]}."""
    # TODO: For each label/options: no options -> warning "<label>: no class at your college counts, take it after transferring",
    #       already done -> skip, otherwise pick_option and add its courses (not completed) to needed with the label.


def prereqs_met(course, completed):
    """Return True if the student has one course from every prereq group; no prereqs means True."""
    # TODO: course["prereqs"] = [["A", "B"], ["C"]] means (A or B) and C.


def add_prereqs(needed, completed, courses):
    """Add missing prereqs (and their prereqs) to needed with reason "Prereq for <course id>"."""
    # TODO: Loop until nothing new is added. If a prereq group has nothing in completed or needed,
    #       add the first course from that group that's in courses.


def open_ge_areas(rules, have, courses, ap_scores, ap_rules):
    """Return the GE areas still empty, e.g. ["1B", "1C"]."""
    # TODO: Each course in have with ge_areas, and each AP exam with score >= min_score, fills ONE spot.
    #       For each rule count the matches; empty spots cycle through the rule's areas ("3A", "3B", "4", ...).


def pick_ge_courses(areas, completed, needed, courses):
    """Return (picks, warnings): the course with the fewest units for each open area, tie -> alphabetical id."""
    # TODO: Skip completed, needed and already picked courses. Reason "GE Area 3A (can swap)".
    #       No course found -> warning "GE Area 3A: no class found at your college".


def build_plan(student, data):
    """Return {"courses": [{"id", "units", "reason"}] sorted by id, "total_units": n, "warnings": [...]}."""
    # TODO: get_major_data -> find_needed_courses -> add_prereqs.
    #       If student["ge_plan"]: open_ge_areas -> pick_ge_courses -> add picks to needed -> add_prereqs again.


def read_json(path):
    """Already done."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_data(folder):
    """Already done. Reads every file in fake_data/ into one dictionary."""
    data = {"courses": {}, "agreements": {}}
    for f in sorted((folder / "courses").glob("*.json")):
        data["courses"][f.stem] = read_json(f)["courses"]
    for f in sorted((folder / "agreements").glob("*.json")):
        a = read_json(f)
        data["agreements"][(a["college"], a["university"], a["program"])] = a
    data["ge_rules"] = {f.stem: read_json(f)["rules"] for f in sorted((folder / "ge_rules").glob("*.json"))}
    data["ap_rules"] = read_json(folder / "ap_rules.json")["rules"]
    return data


def main():
    folder = Path(__file__).with_name("fake_data")
    data = load_data(folder)
    student = read_json(folder / "students" / "student_2.json")
    completed = set(student["completed"])
    courses = {c["id"]: c for c in data["courses"]["chabot"]}
    math_options = [["chabot:MATH 1", "chabot:MATH 2"], ["chabot:MATH 12"]]

    # Test 1: get_major_data
    print("=== get_major_data ===")
    requirements, found_courses, warnings = get_major_data(student, data) or ({}, {}, [])

    # Expected: 12
    print("Requirements:", len(requirements))

    # Expected: 23
    print("Courses:", len(found_courses))

    # Expected: []
    print("Warnings:", warnings)

    # Expected: [['chabot:CS 20'], ['lpc:CS 2']]   (Chabot + LPC options combined)
    requirements, _, _ = get_major_data(read_json(folder / "students" / "student_3.json"), data) or ({}, {}, [])
    print("SJSU: CS 46B:", requirements.get("SJSU: CS 46B"))

    # Expected: 9   (math at SJSU and Berkeley)
    requirements, _, _ = get_major_data(read_json(folder / "students" / "student_6.json"), data) or ({}, {}, [])
    print("Math requirements:", len(requirements))

    # Expected: ['No data yet for lpc to UCB math']
    _, _, warnings = get_major_data(read_json(folder / "students" / "student_4.json"), data) or ({}, {}, [])
    print("Missing data:", warnings)

    # Test 2: requirement_done
    print("\n=== requirement_done ===")

    # Expected: False (only half of the first option)
    print("MATH 1 only:", requirement_done(math_options, {"chabot:MATH 1"}))

    # Expected: True
    print("MATH 1 + MATH 2:", requirement_done(math_options, {"chabot:MATH 1", "chabot:MATH 2"}))

    # Expected: False
    print("No options:", requirement_done([], completed))

    # Test 3: pick_option
    print("\n=== pick_option ===")

    # Expected: ['chabot:MATH 1', 'chabot:MATH 2']   (MATH 1 done, so 5 units left vs 10)
    print("Math:", pick_option(math_options, {"chabot:MATH 1"}, {}, courses))

    # Expected: ['chabot:CS 40']   (3 units vs 4)
    print("Cheaper:", pick_option([["chabot:CS 30"], ["chabot:CS 40"]], set(), {}, courses))

    # Expected: ['chabot:CS 30']   (already needed, so it costs 0)
    print("Already needed:", pick_option([["chabot:CS 40"], ["chabot:CS 30"]], set(), {"chabot:CS 30": ["x"]}, courses))

    # Test 4: find_needed_courses
    print("\n=== find_needed_courses ===")
    test_requirements = {
        "SJSU: CS 46A": [["chabot:CS 10"]],
        "SJSU: CS 46B": [["chabot:CS 20"]],
        "UCB: CS 61B": [["chabot:CS 20"]],
        "SJSU: CS 49J": [],
    }
    needed, warnings = find_needed_courses(test_requirements, completed, courses) or ({}, [])

    # Expected: {'chabot:CS 20': ['SJSU: CS 46B', 'UCB: CS 61B']}   (CS 10 is already completed)
    print("Needed:", needed)

    # Expected: ['SJSU: CS 49J: no class at your college counts, take it after transferring']
    print("Warnings:", warnings)

    # Test 5: prereqs_met
    print("\n=== prereqs_met ===")

    # Expected: True
    print("CS 20:", prereqs_met(courses["chabot:CS 20"], completed))

    # Expected: False (CS 20 has not been completed)
    print("CS 30:", prereqs_met(courses["chabot:CS 30"], completed))

    # Expected: True (no prereqs)
    print("ENGL C1000:", prereqs_met(courses["chabot:ENGL C1000"], completed))

    # Test 6: add_prereqs
    print("\n=== add_prereqs ===")
    needed = {"chabot:CS 30": ["SJSU: CS 47"]}
    add_prereqs(needed, set(), courses)

    # Expected: ['chabot:CS 10', 'chabot:CS 20', 'chabot:CS 30', 'chabot:MATH 1', 'chabot:MATH 5']
    print("After:", sorted(needed))

    # Expected: ['Prereq for chabot:MATH 1']
    print("MATH 5 reason:", needed.get("chabot:MATH 5"))

    # Test 7: open_ge_areas
    print("\n=== open_ge_areas ===")
    golden4 = data["ge_rules"]["golden4"]

    # Expected: ['1B', '1C']
    print("Golden 4:", open_ge_areas(golden4, {"chabot:ENGL C1000", "chabot:MATH 1"}, courses, [], data["ap_rules"]))

    # Expected: ['1A', '1B', '1C']   (AP Calc AB fills Area 2)
    print("With AP:", open_ge_areas(golden4, set(), courses, [{"exam": "Calculus AB", "score": 4}], data["ap_rules"]))

    # Expected: ['3B']   (PHIL 10 counts for 1B or 3B, but only one spot)
    two_rules = [{"areas": ["1B"], "courses": 1}, {"areas": ["3B"], "courses": 1}]
    print("No double counting:", open_ge_areas(two_rules, {"chabot:PHIL 10"}, courses, [], data["ap_rules"]))

    # Expected: ['1A', '1B', '2', '3A', '3B', '4', '5A']
    print("7-course, nothing done:", open_ge_areas(data["ge_rules"]["seven_course"], set(), courses, [], data["ap_rules"]))

    # Test 8: pick_ge_courses
    print("\n=== pick_ge_courses ===")
    picks, warnings = pick_ge_courses(["1B", "1C"], completed, {}, courses) or ({}, [])

    # Expected: {'chabot:ENGL C1001': ['GE Area 1B (can swap)'], 'chabot:COMM C1000': ['GE Area 1C (can swap)']}
    print("Picks:", picks)

    # Expected: ['chabot:ART 1', 'chabot:MUS 10']   (two different 3-unit courses)
    picks, _ = pick_ge_courses(["3A", "3A"], set(), {}, courses) or ({}, [])
    print("Two 3A spots:", sorted(picks))

    # Expected: ['GE Area 9Z: no class found at your college']
    _, warnings = pick_ge_courses(["9Z"], set(), {}, courses) or ({}, [])
    print("No course:", warnings)

    # Test 9: build_plan (needs everything above working)
    print("\n=== build_plan ===")

    # Expected: True for all 6 (open fake_data/students/student_N_expected.json to compare)
    for n in range(1, 7):
        s = read_json(folder / "students" / f"student_{n}.json")
        expected = read_json(folder / "students" / f"student_{n}_expected.json")
        print(f"student_{n}:", build_plan(s, data) == expected)


if __name__ == "__main__":
    main()
