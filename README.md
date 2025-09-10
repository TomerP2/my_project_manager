# Project Management Software

## Info
Author: Tomer Peled (Tomer.a.peled@gmail.com)
Date: 04/09/2025

This project aims to create a program that acts as a project manager for my personal projects.

## Functions

### New project creation
- Create a new project from a chosen template folder.
- Template folder: Contains folders and files.
- Any text 'PROJECT_NAME', either in a file/folder name or file content, will be replaced with the user given project name.
- Any text 'CURRENT_DATE', either in a file/folder name or file content, will be replaced with the current date.
- Option to create an empty .git repository in the project folder
- Option to create an obsidian vault in the project folder

### Project management
- Allows user to archive projects, which zips the project and moves it to the archive.

### Upcoming features
- Allow user to sync project with the template folder, so that changes to the template are reflected in the projects.
- Allow user to zip projects for sharing. Which automatically removes the .env and creates a .env.example file.
- Replace text 'AUTHOR', 'EMAIL', and others with input text.
