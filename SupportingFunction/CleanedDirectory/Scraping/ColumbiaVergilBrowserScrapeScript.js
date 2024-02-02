
// Prework prior to running script
// 1. Filter to COMS courses
// 2. Set view to have 100 courses per page

// Script to paste in browser
// 1. Expand all courses
// Get all the spans with the class "mat-expansion-indicator"
const indicators = document.querySelectorAll('span.mat-expansion-indicator');

// Click on each span
for (let i = 0; i < indicators.length; i++) {
  indicators[i].click();
}

// 2. Get course name data and relevant course description and save to csv.
const expansionPanels = document.querySelectorAll('mat-expansion-panel.accord-course');


const courses = [];
expansionPanels.forEach(panel => {
  const courseNameDiv = panel.querySelector('h3');
  let courseName = "";
  if (courseNameDiv) {
    courseName = courseNameDiv.textContent;
  }

  const courseInfoDev = panel.querySelector('span.identifier');
  let courseInfo = "";
  if (courseInfoDev) {
    courseInfo = courseInfoDev.textContent;
  }

  const courseDescDev = panel.querySelector('div.course-description p');
  let courseDesc = "";
  if (courseDescDev) {
    courseDesc = courseDescDev.textContent;
  }

  courses.push({ name: courseName, info: courseInfo, description: courseDesc });
});

let csvContentOutput = "";

csvContentOutput = "Course Name,Course Info,Course Description\n";
courses.forEach(course => {
  csvContentOutput += `"${course.name}","${course.info}","${course.description}"\n`;
});

const blob = new Blob([csvContentOutput], { type: 'text/csv;charset=utf-8;' });

const link = document.createElement('a');
link.href = URL.createObjectURL(blob);
link.download = 'course_data.csv';

link.click();