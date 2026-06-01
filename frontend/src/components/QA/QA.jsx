import React, { useEffect, useState } from 'react';
import api from '../../api.js';
import SubmitQuestionForm from '../SubmitQuestion/SubmitQuestionForm.jsx';
import './QA.css'

const QASection = () => {
  const [answer, setAnswer] = useState("");
  const [questions, setQuestion] = useState([]);



  const generateAnswer = async (my_question) => {
    setQuestion([{id: Date.now(), text: my_question}])
    setAnswer('...');
    console.log("geneate answer from ", my_question)
    try {
      const response = await api.post('/api/rag/ask', { question: my_question });
      setAnswer(response.data.final_answer);
    } catch (error) {
      console.error("error generating question ", error)
      setAnswer("Sorry, could not generate an answer.");
    }
  };

  return (
    <div className="qa-section">
      {questions.map((question) => (
        <div className="question-container">
          <div className="question-bubble">
              {question.text}
          </div>
        </div>
      ))}
      <div className="response-body">{answer || 'Ask a question to get started.'}</div>
      <SubmitQuestionForm generateAnswer={generateAnswer} />
    </div>
  );
};

export default QASection;
