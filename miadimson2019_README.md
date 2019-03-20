# Mia Dimson's README

## Description:

This project is intended to help teachers and students create goals to help with workflow and getting work done. My part of the project consists of merging the back end to the front end.

Students and teacher can create goals for themselves and delete goals thus far.

## How to run the program:

### Backend:

To run the back end, run:
`cd vagrant` to navigate to the the back end directory,

`vagrant up` to run the virtual machine. Make sure that there is not one already running on the same port

Once `vagrant up` has finished running, run `vagrant ssh`,

Once vagrant ssh is done running, run `cd /vagrant`,

Finally, run `python teacherActions.py`

You may need to install flask_cors for cross-origin resource sharing, to do this, run `sudo pip install -U flask-cors`


### Frontend:

To run the front end, run:
`cd Front-End` to navigate to the front end directory,

Once in the Front-End directory, run `ng serve` to run the front end program

You may need to run `npm install` before running `ng serve` if the program doesn't run correctly


## Tasks to do:

What needs to be done next is to make sure that students and teachers can see their individual goals that they have set for themselves or their students.

Teachers also need to be able to see the progress their students have made on the goals.

Teachers must be able to assign students certain goals and should be able to see the goals that the students have created for themselves.


## Resources:

(https://auth0.com/blog/using-python-flask-and-angular-to-build-modern-apps-part-1)

(https://auth0.com/blog/using-python-flask-and-angular-to-build-modern-web-apps-part-2/)

(https://auth0.com/blog/using-python-flask-and-angular-to-build-modern-web-apps-part-3/)
