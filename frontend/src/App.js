import React, { useState, useEffect } from 'react';
import './App.css';
import background from './background.webp';
import backgroundVideo from './bg.mp4';
import forestImg from './forest.jpg.avif';
import evilGoodImg from './evilgood.jpg.webp';
import familyFriendsImg from './family.jpg';
import adventureImg from './adventure.jpg';

const App = () => {
  const [theme, setTheme] = useState(null);
  const [story, setStory] = useState('');
  const [question, setQuestion] = useState('');
  const [options, setOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState(null);
  const [confirmed, setConfirmed] = useState(false);

  useEffect(() => {
    if (theme) {
      fetchStory();
    }
  }, [theme]);

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
        setSelectedOption(null);
      } catch (error) {
        console.error('Error selecting option:', error);
      } finally {
        setConfirmed(false);
      }
    }
  };

  const themeOptions = [
    { name: 'Forest', image: forestImg },
    { name: 'Evil & Good', image: evilGoodImg },
    { name: 'Family & Friends', image: familyFriendsImg },
    { name: 'Adventure', image: adventureImg }
  ];

  if (!theme) {
    return (
      <div className="App">
        <video autoPlay loop muted className="video-background">
          <source src={backgroundVideo} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        <div className="video-overlay">
          <div className="theme-selection-container">
            <h1>Choose a Theme</h1>
            <ul className="theme-options">
              {themeOptions.map((themeOption, index) => (
                <li key={index} onClick={() => setTheme(themeOption.name)} className="theme-option">
                  <img src={themeOption.image} alt={themeOption.name} className="theme-image" />
                  <p>{themeOption.name}</p>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="App" style={{ backgroundImage: `url(${background})`, backgroundSize: 'cover', backgroundPosition: 'center', height: '100vh', width: '100%' }}>
      {story && (
        <div className="story-container">
          <header className="App-header">
            <p>{story}</p>
          </header>
        </div>
      )}
      {question && (
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


