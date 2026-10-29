import json
from pathlib import Path


def find_course(courses, course_id):
    """Return the matching course dictionary; raise ValueError if not found."""
    # TODO: Loop through courses and compare each course's "id".



def calculate_total_units(courses, planned_courses):
    """Return the sum of planned course units; an empty plan returns 0."""
    # TODO: Use find_course for each planned ID and add its "units".



def check_unit_limit(courses, planned_courses, max_units):
    """Return True when the total units are at or below max_units."""
    # TODO: Reuse calculate_total_units and compare with max_units.



def check_prerequisites(courses, completed_courses, course_id):
    """Return True if all prerequisites are completed; none means True."""
    # TODO: Find the course, then check each ID in its "prerequisites".



def main():
    with Path(__file__).with_name("courses.json").open(
        "r", encoding="utf-8"
    ) as file:
        data = json.load(file)

    courses = data["courses"]
    student = data["student"]
    planned_courses = student["planned_courses"]
    completed_courses = student["completed_courses"]
    max_units = student["max_units"]

    # Test 1: Unit Limit Checker
    print("=== Unit Limit Checker ===")

    # Expected: 13
    print("Total Units:",
          calculate_total_units(courses, planned_courses))

    # Expected: True
    print("Within Unit Limit:",
          check_unit_limit(courses, planned_courses, max_units))

    # Test 2: Prerequisite Checker
    print("\n=== Prerequisite Checker ===")

    # Expected: True
    print("CS15:",
          check_prerequisites(courses, completed_courses, "CS15"))

    # Expected: False (CS15 has not been completed)
    print("CS20:",
          check_prerequisites(courses, completed_courses, "CS20"))

    # Expected: True
    print("ENGL C1000:",
          check_prerequisites(courses, completed_courses, "ENGL C1000"))


if __name__ == "__main__":
    main()
