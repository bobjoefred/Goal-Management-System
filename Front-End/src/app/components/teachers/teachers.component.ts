import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs/Subscription';
import { Teacher } from './teacher.model';
import { TeachersApiService } from './teachers-api.service';
import { Goal } from '../goals/goal.model';
import { GoalsApiService } from '../goals/goals-api.service';

@Component({
  selector: 'app-teachers',
  templateUrl: './teachers.component.html',
  styleUrls: ['./teachers.component.css']
})

export class TeachersComponent implements OnInit {

  teachersListSubs: Subscription;
  teacherList: Array<Teacher>;

  constructor(private readonly teachersApi: TeachersApiService) { }

  ngOnInit(): void {
    this.teachersListSubs = this.teachersApi.getTeachers()
      .subscribe(result => {
        this.teacherList = result;
      });
  }
  // updateGoalTitle(event:any) {
  //   this.goal.goal_name = event.target.value;
  // }
  //
  // updateGoalDescription(event:any) {
  //   this.goal.goalName = event.target.value;
  // }
}
