<div align="center">

<img src="assets/images/automax_logo.png" width="400px">
   
**Automate data science tasks with a button, instead of 600 lines of code**
   
**If it can be automated, assign it to a button**
 
<p align="center">
   <a href="#why-automax-">Why Automax🤔</a> |
   <a href="#quickstart-">Quickstart🚀</a>

</p>

   [![license](https://img.shields.io/github/license/bipinKrishnan/automax)](https://github.com/bipinKrishnan/centroid/blob/main/LICENSE)

   
</div>

_________________________________________________________________________________________

## Why Automax 🤔

With Automax, you can:

* Quickly create a project structure
* Do all of these with the click of a button:

   ♻️ Running workflows
      
   📝 Running unit tests
      
   🕵️ View notebook outputs
      
   📓 Edit python scripts as if they were notebooks 
   
   📊 Get complete profile for a dataset 
   
   🗒️ Get baseline results from a set of models 

## Quickstart 🚀

1. Clone the repo

   ```console
   git clone git@github.com:bipinKrishnan/automax.git
   ```
   
2. Move to the cloned path and run the following commands, automax will create the project with all the required files in the specified project path.
   ```console
   python3 automax <path to project> <project name>
   ```
   
3. Now move to the project path and run this command to launch the dashboard.

   ```console
   make automax-dashboard
   ```
   From now on, the above command is all you need to launch the dashboard.
   
   
 ## TODO
 
 - [ ] Refactor the codebase

 - [ ] Show the complete file structure of the project in the dashboard
 
 - [ ] Make the project into cli tool which is automatically added to the env variable during the first install
 
 - [ ] Add documentation

 - [ ] Add tests and CI

 - [ ] Ability for users to add buttons to automate tasks specific to their projects
