import React, { useEffect, useState, useRef} from 'react';
import api from '../../api.js';
import SubmitQuestionForm from '../SubmitQuestion/SubmitQuestionForm.jsx';
import './QA.css'

function RAGResponse({ text }) {
  return (
    <div className="response-body">
      {text}
    </div>
  );
}

function DisplayQuestion({ question }) {
  return (
    <div className="question-container"  key={question.id}>
      <div className="question-bubble">
          {question.text}
      </div>
    </div>
  );
}


const QASection = () => {
  const [answer, setAnswer] = useState("");
  const [visible, setVisible] = useState(false);
  const [questions, setQuestion] = useState([]);
  const [loading, setLoading] = useState(false);
  const isFirstRender = useRef(true);

  const generateAnswer = async (my_question) => {
    setQuestion([{id: Date.now(), text: my_question}])
    setAnswer('');

    setLoading(true)

    console.log("geneate answer from ", my_question)
    try {
      const response = await api.post('/api/rag/ask', { question: my_question });
      console.log("got the thing!")
      setVisible(true)
      setAnswer(response.data.final_answer); // Triggers typing effect

    } catch (error) {
      console.error("error generating question ", error)
      setAnswer("Sorry, could not generate an answer.");
    } finally {
      setLoading(false);
    }

  };

  return (
    <div className="qa-section">
      {questions.map((question) => (
        <div className="question-container"  key={question.id}>
          <div className="question-bubble">
              {question.text}
          </div>
        </div>
      ))}

      {answer && <RAGResponse text={answer} />}

      <SubmitQuestionForm generateAnswer={generateAnswer} disabled={loading}/>
    </div>
  );
};

export default QASection;
