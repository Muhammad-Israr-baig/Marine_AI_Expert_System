# 🐟 Marine Life Identifier - AI Expert System

An interactive Python application that demonstrates AI reasoning through Forward Chaining and Backward Chaining algorithms to identify marine species and diagnose ecosystem conditions.

## 🌊 Overview

This expert system uses rule-based inference to identify marine life based on observable characteristics. It features two AI reasoning approaches:
- **Forward Chaining (BFS)**: Predicts species from observed facts
- **Backward Chaining (DFS)**: Confirms hypotheses by working backward from goals

## ✨ Features

- 🤖 Dual inference engines (Forward & Backward Chaining)
- 🎨 Modern ocean-themed GUI with real-time logging
- 📊 Step-by-step reasoning visualization
- 🐠 Identifies 4 marine species + coral bleaching detection
- 📚 Educational tool for learning AI reasoning

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.7+
tkinter (included with Python)
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/marine-expert-system.git
cd marine-expert-system
```

2. Run the application:
```bash
python marine_expert_system.py
```

### Optional Enhancement
```bash
pip install ttkbootstrap  # For better UI themes
```

## 📖 Usage

### Forward Chaining (Prediction)
1. Select observed characteristics (color, body shape, habitat, etc.)
2. Click **"RUN FORWARD CHAINING (PREDICT SPECIES)"**
3. View the AI's reasoning process and prediction

**Example:**
```
Selected: Color: Blue, Body Shape: Oval, Habitat: Coral Reef
Result: Species: Blue Tang ✅
```

### Backward Chaining (Confirmation)
1. Select observed facts
2. Choose a goal from the dropdown (e.g., "Species: Lionfish")
3. Click **"RUN BACKWARD CHAINING (CONFIRM GOAL)"**
4. See if the hypothesis can be proven

## 🧠 How It Works

**Forward Chaining (Data → Conclusion)**
- Starts with observations
- Applies rules iteratively
- Derives possible conclusions
- Uses BFS for rule traversal

**Backward Chaining (Goal → Facts)**
- Starts with a hypothesis
- Works backward to find supporting facts
- Recursively checks prerequisites
- Uses DFS for goal proving

## 📚 Knowledge Base

### Identifiable Species

| Species | Required Characteristics |
|---------|-------------------------|
| **Blue Tang** | Blue color + Oval body + Coral reef |
| **Flounder** | Flattened body + Sandy bottom |
| **Lionfish** | Red/White color + Spiky fins + Coral reef |
| **Seahorse** | Tube-like body + Large fan fins + Coral reef |
| **Coral Bleaching** | White/Pale color + Coral reef + High temp |

### Observable Facts

- **Colors**: Blue, Yellow, Red/White, White/Pale
- **Body Shapes**: Flattened, Oval, Tube-like
- **Fins**: Spiky, Large Fan, Caudal Forked
- **Habitats**: Coral Reef, Sandy Bottom, Open Ocean
- **Environment**: High Temperature

## 🎯 Customization

### Add New Species

Edit the `RULES` list:
```python
RULES = [
    ('Species: Clownfish', ["Color: Orange", "Habitat: Coral Reef"]),
    # Your new species here
]
```

### Add New Facts

Update the `ALL_FACTS` list:
```python
ALL_FACTS = [
    "Size: Small",
    "Size: Large",
    # Your new facts here
]
```

## 🗂️ Project Structure
```
marine-expert-system/
│
├── marine_expert_system.py    # Main application
├── sharp_img.png              # App icon (optional)
├── underwater_bg.png          # Background image (optional)
└── README.md                  # This file
```

## 🛠️ Technical Details

- **Language**: Python 3.7+
- **GUI Framework**: Tkinter
- **Algorithms**: BFS (Forward Chaining), DFS (Backward Chaining)
- **Design Pattern**: Rule-based expert system

## 📸 Screenshots

*The application features:*
- Clean observation deck for selecting marine characteristics
- Real-time inference logging windows
- Visual progress indicators during reasoning
- Color-coded results (green for success, red for failure)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Add more marine species
- Improve the UI/UX

## 📄 License

This project is open source and available under the MIT License.

## 🎓 Educational Use

Perfect for:
- AI/ML students learning expert systems
- Understanding inference algorithms
- Demonstrating rule-based reasoning
- Teaching knowledge representation

## 💡 Future Enhancements

- [ ] Add more marine species
- [ ] Include images of species
- [ ] Export reasoning logs
- [ ] Save/load custom knowledge bases
- [ ] Multi-language support

## 📧 Contact

Questions or suggestions? Feel free to open an issue!

israrbaig557799@gmail.com

⭐ **If this project helped you learn about AI expert systems, please give it a star!**

Made with 🐠 and Python
