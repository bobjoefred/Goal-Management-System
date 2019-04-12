# Goal-Management-System
# About
This project at its core allows teachers to assign goals to a student.
The students are able to view the goals assigned to them, and mark those goals  
as completed. Teachers are able to create, view, edit, all students and goals.

# Requirements
- Virtual Box
- Ubuntu Vagrant
- Unix based command line utility

# setUp
- If no Vagrant file exists, put the Ubuntu Vagrant file in the root project director
- Open your Command Line Utility

1. Navigate to /vagrant
2. Input 'vagrant up'
3. Input 'vagrant ssh'
4. Navigate to /vagrant/goal-management
5. delete 'testing.db' if one is present

# Configuration
1. Conduct setup  
2. Confirm that the correct users are given Teacher/Student status

# Operation
1. Conduct setup
2. Input 'python database_populator.py'
3. Input 'python database_setup.py'
4. Input 'python login.py'

# Database Object Explanations
- Student
  - Name: name of the student
  - id: auto-assigned id given to student upon creation
  - email: email address of the student
  - goals: student-goal-link, allowing goals to be linked to a student
  - groups: student-group-link, allowing groups to be linked to a student
- Goal
  - Name: name of the goal
  - id: auto-assigned id given to goal upon creation
  - description: description of goal entailing what the goal is
  - due_date: due date of goal
  - teacher: teacher objected that created the goal
  - students: students who have this goal assigned
- Teacher
  - name: name of teacher
  - id: auto-assigned id given to teacher upon creation
  - login: username corresponding to login information
  - password: password corresponding to login information
- Group
  - name: name of group
  - description: description of group, normally identifying what purpose the group is for(e.g. Group for the Compsci A Class)
  - teacher: teacher that administers the group
  - students: students in the group
  - type: identifies type of group(e.g. advisory, class)
- StudentGoalLink
  - Ties student id's to goals. Upon grouping goal id's with student id's, they are stored through 'students' in the goal class, and 'goals' in the student class(as student/goal objects).
- StudentGroupLink
  - Ties student id's to group. Upon grouping group id's with student id's, they are stored through 'students' in the group class, and 'group' in the student class(as student/group objects).

# TODO
- Implementation of group CRUD into the teachers' side functions
  - Necessary methods are already made/tested in goal-management/teacher_actions.py, and catalog/testing.py  
    respectively
- Implementation of due dates of goals
  - Already implemented in methods, however not used in catalog/login.py
    - Example of usage in catalog/testing.py (specific usage of datetime can be unclear)
# How to:
- For all the actions below, have the server already up and running(go through steps in 'Operation' and 'setup')
- Add student(only works when logged in as a teacher)
  - Click google login button
  - Click 'Add Students Here'
  - Fill in name, click submit
- Add teacher
  - Open database_populator.py in your editor
  - Ensure that the desired teacher to be added is in the populator, and is tied to the correct email
- Assign goal(only works when logged in as a teacher)
  - Click google login button  
  - Click 'Add Goals Here'
  - Fill in fields for goal name('gname'), description, and the name of the student that it needs to be assigned to
- Mark goal as completed
  - Click google login button (teacher or student)
  - Click 'Change Completion Status'
  - Fill in goal name, student name, and click the button for True/False
