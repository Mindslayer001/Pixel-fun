import React, { useState, useEffect } from 'react';
import './App.css';

const App = () => {
  const [story, setStory] = useState('');
  const [question, setQuestion] = useState('');
  const [options, setOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState(null);
  const [confirmed, setConfirmed] = useState(false);

  useEffect(() => {
    fetchStory();
  }, []);

  const fetchStory = async () => {
    try {
      const response = await fetch('http://localhost:8000/');
      const data = await response.json();
      console.log('Fetched data:', data);
      setStory(data.narration);
      setQuestion(data.question);
      setOptions(data.options);
    } catch (error) {
      console.error('Error fetching story:', error);
    }
  };

  const handleOptionSelect = (option) => {
    setSelectedOption(option);
  };

  const handleConfirm = async () => {
    if (selectedOption) {
      try {
        const response = await fetch(`http://localhost:8000/options?option=${encodeURIComponent(selectedOption.choice)}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        const data = await response.json();
        console.log('Response after selecting option:', data);
        setStory(data.narration);
        setQuestion(data.question);
        setOptions(data.options);
        setSelectedOption(null); // Reset the selected option
      } catch (error) {
        console.error('Error selecting option:', error);
      } finally {
        setConfirmed(false); // Reset the confirmation state after updating the story
      }
    }
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
      {question && !confirmed && (
        <div className="question-container">
          <h2>{question}</h2>
          <ul>
            {options.map((option, index) => (
              <li key={index} onClick={() => handleOptionSelect(option)}>
                {option.choice}
              </li>
            ))}
          </ul>
        </div>
      )}
      {selectedOption && !confirmed && (
        <div className="confirmation-container">
          <h2>You selected: {selectedOption.choice}</h2>
          <button onClick={() => setConfirmed(true)}>Confirm</button>
        </div>
      )}
      {confirmed && (
        <div className="confirmation-container">
          <h2>Are you sure you want to proceed with this choice?</h2>
          <button onClick={handleConfirm}>Yes</button>
          <button onClick={() => setConfirmed(false)}>No</button>
        </div>
      )}
    </div>
  );
};

export default App;



