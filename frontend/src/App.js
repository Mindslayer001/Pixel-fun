import React, { useState, useEffect } from 'react';
import './App.css';

const App = () => {
  const [story, setStory] = useState('');
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [selectedOption, setSelectedOption] = useState(null);
  const [options, setOptions] = useState([]);

  const storyText = "Once upon a time in a faraway land, there was a brave knight who sought to find a legendary treasure...";

  const questions = [
    {
      question: "What was the knight seeking?",
      options: [
        { text: "A magical sword", nextStory: "The knight discovered the ancient sword hidden deep within the enchanted forest." },
        { text: "A legendary treasure", nextStory: "The knight embarked on a perilous journey to uncover the mythical treasure of the ancient kings." },
        { text: "A dragon to slay", nextStory: "The knight faced the mighty dragon in a fierce battle to protect the kingdom from its wrath." },
        { text: "A lost kingdom", nextStory: "The knight ventured into the unknown, seeking the lost kingdom of his ancestors." }
      ]
    }
  ];

  useEffect(() => {
    setStory(storyText);

   
    const timer = setTimeout(() => {
      setCurrentQuestion(questions[0]);
      setOptions(questions[0].options);
      setStory(null);  
    }, 8000);

    
    return () => clearTimeout(timer);
  }, []);

  const handleOptionSelect = (option) => {
    setSelectedOption(option);
    setStory(option.nextStory);
    setCurrentQuestion(null);
  };

  return (
    <div className="App">
      {story && (
        <div className="story-container">
          <header className="App-header">
            <p>{story}</p>
          </header>
        </div>
      )}
      {currentQuestion && (
        <div className="question-container">
          <h2>{currentQuestion.question}</h2>
          <ul>
            {options.map((option, index) => (
              <li key={index} onClick={() => handleOptionSelect(option)}>{option.text}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default App;
