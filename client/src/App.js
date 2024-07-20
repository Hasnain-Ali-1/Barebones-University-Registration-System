import React, { useState } from 'react';
import './App.css';

const initialRowState = {
  Student: { studentID: '', studentName: '', creditsEarned: '' },
  Course: { courseID: '', courseTitle: '', instructorID: '', courseCredits: '' },
  Instructor: { instructorID: '', instructorName: '', courseDepartment: '' },
  Enrollment: { enrollmentID: '', studentID: '', courseID: '', studentCourseGrade: '' },
};

function App() {
  const [rows, setRows] = useState([
    { type: 'Student', ...initialRowState['Student'] },
    { type: 'Instructor', ...initialRowState['Instructor'] },
    { type: 'Course', ...initialRowState['Course'] },
    { type: 'Enrollment', ...initialRowState['Enrollment'] },
  ]);

  const handleContentChange = (type, field, value) => {
    const updatedRows = [...rows];
    updatedRows.find((row) => row.type === type)[field] = value;
    setRows(updatedRows);
  };

  const validateFields = (type) => {
    const row = rows.find((row) => row.type === type);
    return Object.values(row).every((value) => value !== '');
  };

// For adding items
const handleAddItem = async (type) => {
  const currentRow = rows.find((row) => row.type === type);

  // Check if creditsEarned is a valid number
  const creditsEarned = parseInt(currentRow.creditsEarned, 10);
  if (type === 'Student' && isNaN(creditsEarned)) {
    console.error('Error: Please enter a valid number for creditsEarned');
    return;
  }
  else {
    if (type === 'Student') {
      currentRow.creditsEarned = creditsEarned;
    }
  }

  // Check if courseCredits is a valid number
  const courseCredits = parseInt(currentRow.courseCredits, 10);
  if (type === 'Course' && isNaN(courseCredits)) {
    console.error('Error: Please enter a valid number for courseCredits');
    return;
  }
  else {
    if (type === 'Course') {
      currentRow.courseCredits = courseCredits;
    }
  }

  // Check if studentCourseGrade is a letter
  if (type === 'Enrollment' && !/^[A-Za-z]$/.test(currentRow.studentCourseGrade)) {
    console.error('Error: Please enter a valid letter for studentCourseGrade');
    return;
  }

  // Check if all fields have data in them
  if (validateFields(type)) {
    try {
      const response = await fetch('http://localhost:5000/add_item', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ type, ...currentRow }),
      });

      const result = await response.json();
      console.log('Data sent for insertion:', { type, ...currentRow });
      console.log(result.message);

      // Reset input values to default
      setRows((prevRows) =>
        prevRows.map((row) => (row.type === type ? { type, ...initialRowState[type] } : row))
      );
    } 
    catch (error) {
      console.error('Error:', error);
    }
  } 
  // If all fields did not have data in them
  else {
    console.error(`Error: Please fill in all fields for ${type}`);
  }
};

const handleDeleteItem = async (index) => {
  const currentRow = rows[index];
  const type = currentRow.type;

  // Check if creditsEarned is a valid number
  const creditsEarned = parseInt(currentRow.creditsEarned, 10);
  if (currentRow.type === 'Student' && isNaN(creditsEarned)) {
    console.error('Error: Cannot delete. Please enter a valid number for creditsEarned');
    return;
  }
  else {
    if (currentRow.type === 'Student') {
      currentRow.creditsEarned = creditsEarned;
    }
  }

  // Check if courseCredits is a valid number
  const courseCredits = parseInt(currentRow.courseCredits, 10);
  if (currentRow.type === 'Course' && isNaN(courseCredits)) {
    console.error('Error: Cannot delete. Please enter a valid number for courseCredits');
    return;
  }
  else {
    if (currentRow.type === 'Course') {
      currentRow.courseCredits = courseCredits;
    }
  }

  // Check if studentCourseGrade is a letter
  if (currentRow.type === 'Enrollment' && !/^[A-Za-z]$/.test(currentRow.studentCourseGrade)) {
    console.error('Error: Cannot delete. Please enter a valid letter for studentCourseGrade');
    return;
  }

  // Check if all fields have data in them
  if (validateFields(currentRow.type)) {
    try {
      const response = await fetch('http://localhost:5000/delete_item', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ type, ...currentRow }),
      });

      const result = await response.json();
      console.log('Data sent for deletion:', { type, ...currentRow });
      console.log(result.message);

      // Reset input values in the text fields to default
      setRows((prevRows) =>
        prevRows.map((row, rowIndex) =>
          rowIndex === index ? { type: row.type, ...initialRowState[row.type] } : row
        )
      );
    } 
    catch (error) {
      console.error('Error:', error);
    }
  }
  // If all fields did not have data in them
  else {
    console.error(`Error: Please fill in all fields for ${currentRow.type}`);
  }
};


  return (
    <div className="App">
      <header className="App-header">
        <h1 className="App-title">CMSC 447 Individual Project</h1>
      </header>
      <main className="App-content">
        {rows.map((row, rowIndex) => (
          <div key={rowIndex} className="row">
            {Object.keys(row)
              .filter((field) => field !== 'type') // Exclude 'type' property
              .map((field) => (
                <input
                  key={field}
                  type="text"
                  value={row[field]}
                  onChange={(e) => handleContentChange(row.type, field, e.target.value)}
                  placeholder={`Enter ${field}`}
                />
              ))}
            <button className="add-button" onClick={() => handleAddItem(row.type)}>
              Add {row.type}
            </button>
            <button className="delete-button" onClick={() => handleDeleteItem(rowIndex)}>
              Delete {row.type}
            </button>
          </div>
        ))}
      </main>
    </div>
  );
}

export default App;
