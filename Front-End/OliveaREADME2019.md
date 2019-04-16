## Olivea Varady's README

## Description:

This project is intended to help teachers and students create goals to help with workflow and getting work done.

My part of the project was to design the front end. So far, the website is fully designed but not functional.

## How to run the program:

### Front End:
To run the front end, run `cd version_control/`

Next, run `cd Goal-Management-System`

Then, run `cd Front-End/`

Finally, run `ng serve`

## Components:

HeaderComponent:
The HeaderComponent is the navbar that is located at the top of the website. The navbar consists of many components which allows one to navigate to different web pages. The HeaderComponent is in charge of separating the Teacher Components from the Student Components. To access the student website, click on the header component and then click on the file labeled header.component.ts. Once in the file, set the "is teacher" to true. To access the teacher website, repeat the same steps above, but set "is teacher" to false.

HomeComponent:
The home component is the login page for both students and teachers. On the student and teacher navbar, the home component is labeled "login".

FooterComponent:
Currently, I have made a footer component but there is no code in it. Once code is added to the footer.component.html and the footer.component.css, the same footer should appear on the bottom of every component.

### Teacher Components:

Assign Component:
The assign component is known as the "assign goals" page on the website. This component is the designed for teachers when they want to assign a specific goal to a student or multiple students. Currently, the page is not functional.

Individual Component:
The individual component is known as the "Individual Students" page on the website. This page allows teachers to view individual student progress through a table. This page is not linked to the backend so the page is just a design.

Teachers Component:
The teacher component is known as "home" on the website. This page is the home page for teachers. This page lists what classes the teachers teach and the overarching theme of each class. Again, this page is not functional and is design only. 

### Student Components:

Student-History Component:

Student-Individual Component:

Student-Reject Component:

Students Component:

## Tasks To-Do:
Currently, the header thinks the page is collapsed, so you need to make the header expand across the whole top of the page.

Add Code into the footer component in order to have the same footer on every page.

If we want Chadwick to use this website, we need to make the page fully functional. You must merge with backend to see what is functional and what is not.
