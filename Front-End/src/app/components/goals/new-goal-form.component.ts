import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { GoalsApiService } from './goals-api.service';
import { Observable } from 'rxjs/Observable';

@Component({
  selector: 'app-new-goal-form',
  templateUrl: './new-goal-form.component.html',
  styleUrls: ['./goals.component.css']
})

export class NewGoalFormComponent {
  goal = {
    goalName: '',
    description: ''
  };

  constructor(private readonly goalsApi: GoalsApiService, private readonly router: Router) { }

  updateGoalTitle(event: any): Observable<any> {
    this.goal.goalName = event.target.value;
  }

  updateGoalDescription(event: any): Observable<any> {
    this.goal.description = event.target.value;
  }

  saveGoalTeacher(event: any): Observable<any> {
    this.goalsApi
      .saveGoalTeacher(this.goal)
      .subscribe(
        () => this.router.navigate(['teacher/goals']),
        error => alert
        (error.message)
      );
  }

  saveGoalStudent(event: any): Observable<any> {
    this.goalsApi
      .saveGoalStudent(this.goal)
      .subscribe(
        () => this.router.navigate(['student/goals']),
        error => alert
        (error.message)
      );
  }
}
