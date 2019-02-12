import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { GoalsApiService } from './goals-api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'new-goal-form',
  templateUrl: './new-goal-form.component.html',
  styleUrls: ['./goals.component.css']
})

export class NewGoalFormComponent {
  goal = {
    goalName: '',
    description: ''
  };

  constructor(private goalsApi: GoalsApiService, private router: Router) { }

  updateGoalTitle(event: any) {
    this.goal.goalName = event.target.value;
  }

  updateGoalDescription(event: any) {
    this.goal.description = event.target.value;
    console.log(event.target.value)
  }

  saveGoal() {
    this.goalsApi
      .saveGoal(this.goal)
      .subscribe(
        () => this.router.navigate(['teacher/goals']),
        error => alert(error.message)
      );
  }
}
