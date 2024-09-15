# PixelFun: Interactive Story Generator

### 🏆 **Hackathon Project**

Pixel fun is an innovative and interactive story-generating application where users—primarily children—can explore and shape the narrative by making decisions at key points. Through an engaging, safe, and educational platform, Pixel-fun aims to cultivate wisdom and maturity in young players while delivering a fun and immersive experience.

## 🚀 Project Overview

**Goal**:  
The primary purpose of Pixel-fun is to provide a safe, fun, and educational environment for children, enabling them to learn valuable life lessons through interactive storytelling. As users make choices throughout the story, they learn the consequences of their decisions, helping them grow wiser and more mature in a playful setting.

**Why This Matters**:  
In today's digital age, many children are exposed to games that may not foster the best values. Pixel-fun fills this gap by offering an alternative that's entertaining, thought-provoking, and free from offensive content. It's a game parents can trust and children can enjoy!

---

## 🎮 How It Works

1. **Start the Journey**:  
   Players enter an imaginative world where the story unfolds with each step.
   
2. **Choose Your Path**:  
   At every significant point in the story, players are presented with multiple options to choose from. Each decision impacts the direction the story takes.
   
3. **Learn & Grow**:  
   With every decision, players discover the consequences of their actions, encouraging them to think critically about their choices.

4. **AI-Powered Stories**:  
   The stories are dynamically generated using cutting-edge AI technology, making every playthrough unique.

---

## 🛠️ Tech Stack

- **Frontend**: React.js – For a responsive and intuitive user interface.
- **Backend**: FastAPI – For efficient API handling and smooth communication between frontend and backend.
- **AI Engine**: LLaMA 3 (8B) – A large language model that generates dynamic and engaging stories based on user input.

---

## ✨ Features

- **Interactive Storytelling**: Users can control the flow of the story by selecting different actions at critical points.
- **Child-Safe Environment**: No offensive content or inappropriate themes.
- **Dynamic Story Generation**: Using LLaMA 3 (8B), the application generates unique stories in real-time, ensuring a fresh experience every time.
- **Educational Value**: Helps children understand the importance of decision-making and consequences in a fun and engaging manner.
- **User-Friendly Interface**: Simple, clean, and intuitive UI built with React.js.
- **Fast & Efficient**: Powered by FastAPI, ensuring quick responses to user inputs.

---

## 💡 Motivation

Pixel-fun was developed in just **3 days** as part of a hackathon. The inspiration came from the desire to provide children with a meaningful and fun alternative to many of the offensive and violent games currently dominating the market. By combining advanced AI and interactive storytelling, we wanted to create a tool that not only entertains but also teaches children valuable lessons.

---

## 🚧 Challenges Faced

- **Time Constraints**: Building an interactive, AI-driven storytelling platform within 3 days required significant planning and rapid execution.
- **AI Integration**: Integrating LLaMA 3 (8B) into the application for real-time story generation was a complex but rewarding task.
- **User Experience**: Ensuring the platform was both engaging and easy to use for children posed design challenges.

---

## 🧑‍💻 How to Run Locally

To run this project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Pixel-fun.git
   cd Pixel-fun
   ```

2. **Install frontend dependencies**:
   ```bash
   cd frontend
   npm install
   ```

3. **Install backend dependencies**:
   ```bash
   cd ../fastapi
   pip install -r requirements.txt
   ```

4. **Go to groq AI offical website and get your credentials(free)**:
   ```bash
   touch .env
   echo "STORY_API=your_api_key_here" >> .env
   ```

5. **Start the backend**:
   ```bash
   uvicorn main:app --reload
   ```

5. **Start the frontend**:
   ```bash
   cd ../frontend
   npm start
   ```

6. Open your browser and navigate to `http://localhost:3000` to access the app.

---

## 📚 Future Improvements

- **Expand Story Library**: Add more pre-defined story arcs to enhance the diversity of scenarios.
- **More AI Models**: Integrate additional language models to provide more nuanced and personalized storytelling.
- **User Profiles**: Allow users to create profiles and save their progress across multiple stories.
- **Multilingual Support**: Introduce language options to make the app accessible to children around the world.

---

## 🙌 Contributions

We welcome contributions to make Pixel-fun even better! If you're interested in contributing:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

---

## 💬 Feedback

Your feedback is valuable to us! Feel free to open an issue or submit a feature request. We're always looking to improve!

---

## 🧾 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## 🤝 Acknowledgments

- **LLaMA Team** for providing the LLaMA 3 model.
- The hackathon organizers for giving us the opportunity to work on this project.
- All contributors and testers who helped along the way.
