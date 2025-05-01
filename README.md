# Space Shooter

A dynamic space shooter game where you defend the cosmos from waves of enemies!

![alt text](https://raw.githubusercontent.com/veryyynice/pygame-Space-Shooter/master/screenshot.png "Logo Title Text 1")
## 🚀 Features

- **Engaging Gameplay**: Navigate through space, shoot enemies, and rack up your score
- **Charge Shots**: Hold the space bar to charge larger, more powerful bullets
- **Dynamic Ship Sizing**: Resize your ship during gameplay with mouse clicks
- **Level System**: Two distinct levels with different enemy speeds and backgrounds
- **Save/Load System**: Continue your game from where you left off
- **Sound Effects**: Immersive audio experience with sound effects and background music
- **Intro Videos**: Cool level introductions using OpenCV video integration

## 🎮 Controls

- **Arrow Keys**: Move your ship
- **Space Bar**: Shoot (hold to charge for larger bullets)
- **Left Mouse Click**: Increase ship size
- **Right Mouse Click**: Decrease ship size
- **ESC**: Pause game

## 📋 Requirements

- Python 3.6+
- Pygame
- OpenCV (cv2)
- NumPy

## 💻 Installation

1. Clone this repository:
   ```
   git clone https://github.com/veryyynice/pygame-Space-Shooter.git
   cd cosmic-defender
   ```

2. Install the required packages:
   ```
   pip install pygame opencv-python numpy
   ```

3. Create the following directories if they don't exist:
   ```
   mkdir sounds videos
   ```

3 continued Add your own sound files to the `sounds` directory:
   - `shoot.wav` - Sound effect when shooting
   - `explosion.wav` - Sound when player collides with an enemy
   - `elevator.mp3` - Music during pause
   - `theme.mp3` - Main background music

3 continued Add your video files to the `videos` directory:
   - `insert_coin.mp4` - Video to play when starting level 2

## 🎯 How to Play

Run the game:
```
python main.py
```

1. From the main menu, select "Start Game" to begin a new game at level 1
2. Choose "Load Game" to continue from your last saved position
3. Select "Select Level" to choose which level to play
4. Survive as long as possible and achieve the highest score!

## 🛠️ Game Mechanics

- **Enemy Spawning**: Enemies appear from the right side of the screen at different speeds
- **Scoring**: Earn 10 points for each enemy you destroy
- **Game Over**: The game ends when an enemy collides with your ship
- **Auto-Save**: Your progress is automatically saved when the game ends

## 🚧 Future Improvements

- Add more enemy types with different behaviors
- Implement power-ups and special abilities
- Create additional levels with increasing difficulty
- Add a high score leaderboard

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/veryyynice/pygame-Space-Shooter/issues).

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Original game by Tom Strzyz
- Modified to include sound effects and OpenCV video support
