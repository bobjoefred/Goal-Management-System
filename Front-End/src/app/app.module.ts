import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { Routes, RouterModule} from '@angular/router';
// import {MatToolbarModule} from '@angular/material/toolbar';

import { AppComponent } from './app.component';
import { HeaderComponent } from './components/header/header.component';
import { HomeComponent } from './components/home/home.component';
import { FooterComponent } from './components/footer/footer.component';
import { TeachersComponent } from './components/teachers/teachers.component';
import { StudentsComponent } from './components/students/students.component';
import { IndividualComponent } from './components/individual/individual.component';
import { TeachersApiService } from './components/teachers/teachers-api.service';
import { AssignComponent } from './assign/assign.component';

const appRoutes: Routes = [
  {path: 'home', component: HomeComponent },
  {path: 'teachers', component: TeachersComponent},
  {path: 'students', component: StudentsComponent},
  {path: 'individual', component: IndividualComponent}
]

@NgModule({
  declarations: [
    AppComponent,
    FooterComponent,
    HeaderComponent,
    HomeComponent,
    TeachersComponent,
    StudentsComponent,
    IndividualComponent,
    AssignComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    RouterModule.forRoot(appRoutes)
],

  providers: [TeachersApiService],
  bootstrap: [AppComponent]
})
export class AppModule { }
