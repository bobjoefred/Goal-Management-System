# Goal-Management-System
#About
This project at its core allows teachers to assign goals to a student.
The students are able to view the goals assigned to them, and mark those goals  
as completed. Teachers are able to create, view, edit, all students and goals.

#Requirements
- Virtual Box
- Ubuntu Vagrant
- Unix based command line utility

#setUp
- If no Vagrant file exists, put the Ubuntu Vagrant file in the root project director
- Open your Command Line Utility

1. Navigate to /vagrant
2. Input 'vagrant up'
3. Input 'vagrant ssh'
4. Navigate to /vagrant/goal-management
5. delete 'testing.db' if one is present

#Configuration
1. Conduct setup  
2. Confirm that the correct users are given Teacher/Student status

#Operation
1. Conduct setup
2. Input 'python database_setup.py'
3. Input 'python login.py'

#TODO
- Implementation of group CRUD into the teachers' side functions
  - Necessary methods are already made/tested in catalog/teacher_actions.py, and catalog/testing.py  
    respectively
- Implementation of due dates of goals
  - Already implemented in methods, however not used in catalog/login.py
    - Example of usage in catalog/testing.py (specific usage of datetime can be unclear)



make stuff in login.py(login and create studdnts n shit)
