# Clash in Space

[![Build Desktop Executables](https://github.com/ShivamKR12/Clash-in-Space/actions/workflows/build.yml/badge.svg)](https://github.com/ShivamKR12/Clash-in-Space/actions/workflows/build.yml)

A classic arcade-style space shooter game built with Python and Pygame Community Edition. Dodge and destroy asteroids, fight for the high score!

## 🚀 Features

*   Classic top-down space shooter gameplay.
*   Engaging sound effects and background music.
*   Explosive visual effects.
*   Cross-platform support (Windows, macOS, and Linux).

## 🎮 Getting Started

You can easily play the game by downloading the latest version for your operating system.

1.  Go to the [**Releases**](https://github.com/ShivamKR12/Clash-in-Space/releases) page.
2.  Download the appropriate file for your system (Windows, macOS, or Linux).
3.  Unzip the file and run the `clash-in-space` executable.

**Note:** You may need to grant permissions for the application to run on macOS and Linux.

## 🕹️ How to Play

*   **Arrow Keys/WASD:** Move your ship.
*   **Spacebar:** Fire lasers.
*   **Escape:** Quit the game.

## 🛠️ Building From Source

If you want to build the game yourself, you'll need Python 3 and some dependencies.

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/ShivamKR12/Clash-in-Space.git
    cd Clash-in-Space
    ```

2.  **Create a virtual environment (recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```sh
    pip install pygame-ce pyinstaller
    ```

4.  **Run the game:**
    ```sh
    python main.py
    ```

5.  **Build the executable:**
    This project uses PyInstaller to create standalone executables.
    ```sh
    pyinstaller Clash-in-Space.spec
    ```
    The final executable will be in the `dist/` directory.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
