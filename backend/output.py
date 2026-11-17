import json
class Course: # convert this sample class to json
    # stuff known already known
    courseTitle: str
    courseSubject: str
    courseNumber: str
    units: int
    # stuff needing to be calculated before function call
    preRequirements = [] # what classes are needed for this course (need to determine if this should be an id to prereqs or just the name of said prereq)
    genEdFulfillment = [] # what areas of CalGETC does this cover?
    useableForSchools = [] # what schools need this
    def __init__(self, t: str, s: str, n: str, u: int, p: list[str], g: list[str], U: list[str]): # simple class constructor
        self.courseTitle = t
        self.courseSubject = s 
        self.courseNumber = n
        self.units = u 
        self.preRequirements = p
        self.genEdFulfillment = g 
        self.useableForSchools = U

# sample dict: 
# dictionary = {"Chabot": [], "lasPositas": []}
# Each key must contain a list of Course objects

# Template function for outputting data from algorithms to front via json
def User_Courses(result: dict[str, list[Course]]): # argument : dict
    output = [] # what will be outputted into a Json
    indent = 0 # counts number of indents (kinda like number of lines) we need
    for college in result: # loops through the colleges
        temp = { # temp be a single dict with college as it's key
            college: [] 
        }
        for course in result[college]: # loops through the college's courses
            courseTemp = { # temp object for each course
                "title": course.courseTitle,
                "subject": course.courseSubject,
                "number": course.courseNumber,
                "units": course.units,
                "preReq":course.preRequirements,
                "genEd": course.genEdFulfillment,
                "forSchools": course.useableForSchools
            }
            indent += 1 # indent per course
            temp[college].append(courseTemp) # appends the course into it's college dict
        output.append(temp) # appends the college into the output dict
        indent+=1 # indent per college
        
    with open("result.json", "w") as file:
        json.dump(output,file, indent=indent) # dumps output dict into a json format

# Sample test Code : 
# a = Course("Introduction to Programming C++","CSCI", "14", 3, ["MTH55"],[],["SJSU"])
# b = Course("Calcus II", "MTH", "2", 5,["MTH1"],["Area 2", "Area 4"],["SJSU"])
# c = Course("General Physics I","PHYS","1A",5,["MTH2"],["Area 5A"],["SJSU"])
# d = {"Chabot": [a,b], "LasPositas": [c]}
# User_Courses(d)
# Sample Output: 
# [
#      {
#           "Chabot": [
#                {
#                     "title": "Introduction to Programming C++",
#                     "subject": "CSCI",
#                     "number": "14",
#                     "units": 3,
#                     "preReq": [
#                          "MTH55"
#                     ],
#                     "genEd": [],
#                     "forSchools": [
#                          "SJSU"
#                     ]
#                },
#                {
#                     "title": "Calcus II",
#                     "subject": "MTH",
#                     "number": "2",
#                     "units": 5,
#                     "preReq": [
#                          "MTH1"
#                     ],
#                     "genEd": [
#                          "Area 2",
#                          "Area 4"
#                     ],
#                     "forSchools": [
#                          "SJSU"
#                     ]
#                }
#           ]
#      },
#      {
#           "LasPositas": [
#                {
#                     "title": "General Physics I",
#                     "subject": "PHYS",
#                     "number": "1A",
#                     "units": 5,
#                     "preReq": [
#                          "MTH2"
#                     ],
#                     "genEd": [
#                          "Area 5A"
#                     ],
#                     "forSchools": [
#                          "SJSU"
#                     ]
#                }
#           ]
#      }
# ]