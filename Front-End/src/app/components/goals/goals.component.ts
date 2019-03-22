import { Component, OnDestroy, OnInit } from '@angular/core';
import { Goal } from './goal.model';
import { GoalsApiService } from './goals-api.service';
import { Observable } from 'rxjs/Observable';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'app-goals',
  templateUrl: './goals.component.html',
  styleUrls: ['./goals.component.css']
})
export class GoalsComponent implements OnInit {

  goalsListSubs: Subscription;
  goalsList: Array<Goal>;
  goals: Array<Goal>;

  constructor(private readonly goalsApi: GoalsApiService) {

  }

  ngOnInit() {
    this.goalsListSubs = this.goalsApi
      .getGoalsStudent()
      .subscribe(res => {
        this.goalsList = res;
      },
        console.error
      );
  }

  deleteGoalTeacher(GOAL_ID: number): void {
    this.goalsApi
      .deleteGoalTeacher(GOAL_ID)
      .subscribe(() => {
        this.goalsListSubs = this.goalsApi
          .getGoalsTeacher()
          .subscribe(res => {
            this.goalsList = res;
          },
            console.error
          );
      }, console.error);
  }

  deleteGoalStudent(GOAL_ID: number): void {
    this.goalsApi
      .deleteGoalStudent(GOAL_ID)
      .subscribe(() => {
        this.goalsListSubs = this.goalsApi
          .getGoalsStudent()
          .subscribe(res => {
            this.goalsList = res;
          },
            console.error
          );
      }, console.error);
  }

}
