# PLACEHOLDER

## Info
Author: Tomer Peled (Tomer.Peled@Wur.nl)
Date: 04/09/2025

This project aims to create a program that acts as a project manager for my personal projects.

## Functions

### New project creation
- Create a new project from a chosen template folder.
- Template folder: Contains folders and files.
- Any text 'PROJECT_NAME', either in a file/folder name or file content, will be replaced with the user given project name.
- Any text 'CURRENT_DATA' will be replaced with the current date.

### Project management
- Allows user to sync project with the template folder, so that changes to the template are reflected in the projects
- Allows user to zip projects for sharing. Which automatically removes the .env and creates a .env.example file. 
- Allows user to archive projects, which zips the project and moves it to the archive, sorted by date.
