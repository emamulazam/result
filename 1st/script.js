let csvData = [];

const subjects = {
  "211501": ["History of the Emergence of Independent Bangladesh", 4],
  "212209": ["Principles of Economics", 4],
  "212211": ["Bangladesh Agricultural Economics", 2],
  "213601": ["Introductory Statistics", 4],
  "213603": ["Introductory Probability & Numerical Mathematics", 4],
  "213604": ["Lab 1: Descriptive Statistics", 2],
  "213606": ["Lab 2: Numerical Mathematics", 2],
  "213709": ["Fundamentals of Mathematics", 4],
  "213711": ["Calculus-I", 2],
};

const gradePoints = {
  "A+": 4.0, "A": 3.75, "A-": 3.5,
  "B+": 3.25, "B": 3.0, "B-": 2.75,
  "C+": 2.5, "C": 2.25, "D": 2.0,
  "Fail": 0.0, "F": 0.0
};

function parseCSV(text) {
  const lines = text.trim().split("\n");
  const headers = lines[0].split(",").map(h => h.trim());
  return lines.slice(1).map(line => {
    const values = line.split(",").map(v => v.trim());
    const obj = {};
    headers.forEach((h, i) => obj[h] = values[i]);
    return obj;
  });
}

function fetchCSV() {
  fetch('result.csv')
    .then(response => {
      if (!response.ok) throw new Error("CSV file not found");
      return response.text();
    })
    .then(text => {
      csvData = parseCSV(text);
    })
    .catch(error => {
      document.getElementById("result").innerHTML = `<p>Error loading CSV: ${error}</p>`;
    });
}

function searchResult() {
  const reg = document.getElementById("regInput").value.trim();
  const student = csvData.find(s => s["Registration"] === reg);

  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "";

  if (!student) {
    resultDiv.innerHTML = `<p>No student found with registration: ${reg}</p>`;
    return;
  }

  let totalCredits = 0;
  let earnedCredits = 0;
  let weightedScore = 0;
  let failCount = 0;

  let table = `
    <h2>${student.Name}</h2>
    <p><strong>Roll:</strong> ${student.Roll}</p>
    <p><strong>Registration:</strong> ${student.Registration}</p>
    <table>
      <tr>
        <th>Code</th>
        <th>Subject</th>
        <th>Grade</th>
        <th>Credit</th>
      </tr>
  `;

  for (let code in subjects) {
    const [subjectName, credit] = subjects[code];
    const grade = (student[code] || "N/A").trim();
    const point = gradePoints.hasOwnProperty(grade) ? gradePoints[grade] : 0;

    totalCredits += credit;
    if (grade !== "Fail" && grade !== "F" && grade !== "N/A") {
      earnedCredits += credit;
      weightedScore += point * credit;
    } else {
      failCount++;
    }

    table += `
      <tr>
        <td>${code}</td>
        <td>${subjectName}</td>
        <td>${grade}</td>
        <td>${credit}</td>
      </tr>
    `;
  }

  const cgpa = (weightedScore / totalCredits).toFixed(2);
  const promoted = failCount <= 5 ? "Yes" : "No";
  let classification = "Fail";
  if (cgpa >= 3.00) classification = "1st";
  else if (cgpa >= 2.50) classification = "2nd";
  else if (cgpa >= 2.00) classification = "3rd";

  table += `</table>
    <p><strong>Total Credits:</strong> ${totalCredits}</p>
    <p><strong>Credits Earned:</strong> ${earnedCredits}</p>
    <p><strong>CGPA:</strong> ${cgpa}</p>
    <p><strong>Class:</strong> ${classification}</p>
    <p><strong>Promoted:</strong> ${promoted}</p>
  `;

  resultDiv.innerHTML = table;
}

window.onload = fetchCSV;
