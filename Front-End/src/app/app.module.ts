import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule, Routes } from '@angular/router';
// import {MatToolbarModule} from '@angular/material/toolbar';

import { AppComponent } from './app.component';
import { AssignComponent } from './components/assign/assign.component';
import { FooterComponent } from './components/footer/footer.component';
import { GoalsApiService } from './components/goals/goals-api.service';
import { GoalsComponent } from './components/goals/goals.component';
import { NewGoalFormComponent } from './components/goals/new-goal-form.component';
import { HeaderComponent } from './components/header/header.component';
import { HomeComponent } from './components/home/home.component';
import { IndividualComponent } from './components/individual/individual.component';
<<<<<<< HEAD
import { ResourcesMenuComponent } from './components/resources-menu/resources-menu.component';
import { StudentHistoryComponent } from './components/student-history/student-history.component';
import { StudentIndividualComponent } from './components/student-individual/student-individual.component';
=======
import { StudentHistoryComponent } from './components/student-history/student-history.component';
import { StudentIndividualComponent } from './components/student-individual/student-individual.component';
import { StudentRejectComponent } from './components/student-reject/student-reject.component';
>>>>>>> ovarady/frontend-backend-connection
import { StudentsComponent } from './components/students/students.component';
import { TeachersApiService } from './components/teachers/teachers-api.service';
import { TeachersComponent } from './components/teachers/teachers.component';

const appRoutes: Routes = [
<<<<<<< HEAD
  { path: 'assign', component: AssignComponent },
  { path: 'home', component: HomeComponent },
  { path: 'individual', component: IndividualComponent },
  { path: 'students', component: StudentsComponent },
  { path: 'student/goals', component: GoalsComponent },
  { path: 'student/goals/new', component: NewGoalFormComponent },
  { path: 'students-individual', component: StudentIndividualComponent },
  { path: 'students-history', component: StudentHistoryComponent },
  { path: 'teacher', component: TeachersComponent },
  { path: 'teacher/goals', component: GoalsComponent },
  { path: 'teacher/goals/new', component: NewGoalFormComponent }

=======
  {path: 'assign', component: AssignComponent},
  {path: 'home', component: HomeComponent },
  {path: 'individual', component: IndividualComponent},
  {path: 'students', component: StudentsComponent},
  {path: 'students-individual', component: StudentIndividualComponent},
  {path: 'students-history', component: StudentHistoryComponent},
  {path: 'student-reject', component: StudentRejectComponent},
  {path: 'teachers', component: TeachersComponent}
>>>>>>> ovarady/frontend-backend-connection
];

@NgModule({
  declarations: [
    AppComponent,
    AssignComponent,
    FooterComponent,
    HeaderComponent,
    HomeComponent,
    IndividualComponent,
    StudentsComponent,
    StudentIndividualComponent,
    StudentHistoryComponent,
    TeachersComponent,
<<<<<<< HEAD
    GoalsComponent,
    NewGoalFormComponent,
    ResourcesMenuComponent
=======
    StudentRejectComponent
>>>>>>> ovarady/frontend-backend-connection
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    RouterModule.forRoot(appRoutes)
],
  bootstrap: [AppComponent],
  providers: [TeachersApiService, GoalsApiService]

})
export class AppModule { }
