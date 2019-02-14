import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs/Subscription';
import { Goal } from './goal.model';
import { GoalsApiService } from './goals-api.service';
import { Observable } from 'rxjs/Observable';

@Component({
  selector: 'app-goals',
  templateUrl: './goals.component.html',
  styleUrls: ['./goals.component.css']
})
export class GoalsComponent implements OnInit {

  goalsListSubs: Subscription;
  goalsList: Array<Goal>;
  goals: Array<Goal>;

  constructor(private goalsApi: GoalsApiService) {

  }

  ngOnInit() {
    // this.goalsListSubs = this.goalsApi
    //   .getGoalsTeacher()
    //   .subscribe(res => {
    //       this.goalsList = res;
    //     },
    //     console.error
    //   );

    this.goalsListSubs = this.goalsApi
      .getGoalsStudent()
      .subscribe(res => {
          this.goalsList = res;
        },
        console.error
      );
  }

  ngOnDestroy() {
    this.goalsListSubs.unsubscribe();
  }

deleteGoalTeacher(GOAL_ID: number) {
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

deleteGoalStudent(GOAL_ID: number) {
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
