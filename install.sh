#!/bin/bash
#
# Shell script to install dependencies for the AI-Powered Shell on Debian-based systems (like Debian, Ubuntu, etc.).
#
# How to run:
# 1. Open your terminal.
# 2. Navigate to the directory where you saved this script.
# 3. Make the script executable: chmod +x install.sh
# 4. Run the script: ./install.sh

echo -e "\033[1;32m--- AI-Powered Shell Installer for Debian-based Systems ---\033[0m"

# --- Update package list ---
echo -e "\n\033[1;34m[1/3] Updating package lists...\033[0m"
if ! sudo apt-get update; then
    echo -e "\033[1;31mError: Failed to update package lists. Please check your internet connection and repository configuration.\033[0m"
    exit 1
fi

# --- Install Python and Pip ---
echo -e "\n\033[1;34m[2/3] Installing Python3 and Pip...\033[0m"
if ! sudo apt-get install -y python3 python3-pip; then
    echo -e "\033[1;31mError: Failed to install Python. Please check your system's package manager.\033[0m"
    exit 1
fi

# --- Install Python Dependencies ---
echo -e "\n\033[1;34m[3/3] Installing required Python packages...\033[0m"
if ! pip3 install requests google-generativeai; then
    echo -e "\033[1;31mError: Failed to install Python packages. Please ensure pip3 is working correctly.\033[0m"
    exit 1
fi

echo -e "\n\033[1;32m--- Installation Complete ---\033[0m"
echo -e "You can now run the main script by typing: \033[1;35mpython3 ai_shell-alpha0.0.20.py\033[0m"
echo -e "\n\033[1;33mNOTE: For 'Metasploit Assistant' mode, you must install the Metasploit Framework separately.\033[0m"
echo -e "\033[1;33mYou can find installation instructions on the official Rapid7 website.\033[0m"

