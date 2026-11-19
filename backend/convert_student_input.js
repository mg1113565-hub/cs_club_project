const fs = require("fs");

function convertToJSON(formData) {

    // Create an object to store the student's information
    const studentInput = {

        // Get the universities and majors the student selected
        transfer_targets: formData.universities.map(item => ({
            university: item.university,
            major: item.major
        })),

        // Get the community colleges the student attends
        community_college_courses: formData.colleges.map(college => ({
            // Get the name of the community college
            college: college.name,
            // Get the courses taken or planned at that college
            courses: college.courses.map(course => ({
                id: course.id,
                status: course.status
            }))
        })),

        // Get the student's AP subjects and scores
        ap_scores: formData.apScores.map(ap => ({
            subject: ap.subject,
            // Convert the score into a number
            score: Number(ap.score)
        })),

        // Get the term and year the student wants to transfer
        transfer_term: {
            term: formData.transferTerm.term,
            // Convert the year into a number
            year: Number(formData.transferTerm.year)
        }
    };

    // Convert the student information into a JSON string
    return JSON.stringify(studentInput, null, 2);
}


// Frontend Input
const formData = {

    universities: [
        {
            university: "University of California, Berkeley",
            major: "Computer Science"
        },
        {
            university: "San Jose State University",
            major: "Mathematics"
        }
    ],

    colleges: [
        {
            name: "Chabot College",
            courses: [
                { id: "CS14", status: "Completed" },
                { id: "MATH1", status: "Completed" }
            ]
        },
        {
            name: "Las Positas",
            courses: [
                { id: "CS20", status: "planned" },
                { id: "MATH2", status: "planned" }
            ]
        }
    ],

    apScores: [
        { subject: "AP Calculus AB", score: 5 },
        { subject: "AP Calculus BC", score: 5 },
        { subject: "AP Physics", score: 5 }
    ],

    transferTerm: {
        term: "Fall",
        year: 2028
    }
};


const jsonOutput = convertToJSON(formData);
fs.writeFileSync("student_input.json", jsonOutput, "utf8");

