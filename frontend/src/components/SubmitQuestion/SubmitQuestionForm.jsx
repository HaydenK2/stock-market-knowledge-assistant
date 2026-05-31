import React, { useState } from 'react';
import './SubmitQuestion.css'

const SubmitQuestionForm = ({ generateAnswer }) => {
  const [questionName, setQuestionName] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    if (questionName) {
      console.log("question is ", questionName)
      generateAnswer(questionName);
      setQuestionName('');
    }
  };

  return (
    <div className="form-container">
      <div className="submit-form-components">
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={questionName}
            onChange={(e) => setQuestionName(e.target.value)}
            placeholder="Enter Your Question Here"
          />
          <button type="submit"> ^ </button>
        </form>
      </div>
    </div>


  );
};

export default SubmitQuestionForm;
