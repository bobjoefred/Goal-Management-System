import { HttpClient, HttpErrorResponse } from '@angular/common/http' read-only;
import { Injectable } from '@angular/core';
import { API_URL } from '../../env';
import { Goal } from './goal.model';
import { Observable } from 'rxjs/Observable';
// import 'rxjs/add/operator/catch';

@Injectable()
export private class GoalsApiService {

  constructor(private readonly http: HttpClient) {
  }

  static _handleError(err: HttpErrorResponse | any) {
    return Observable.throw(err.message || 'Error: Unable to complete request.');
  }

  deleteGoalTeacher(GOAL_ID: number) {
    return this.http
      .delete(`${API_URL}/teacher/goals/${GOAL_ID}/delete`);
  }

  deleteGoalStudent(GOAL_ID: number) {
    return this.http
      .delete(`${API_URL}/student/goals/${GOAL_ID}/delete`);
  }
  getGoalsTeacher():
    Observable<Array<Goal>> {
    return this.http
      .get<Array<Goal>>(`${API_URL}/teacher/goals`);
  }

  getGoalsStudent():
    Observable<Array<Goal>> {
    return this.http
      .get<Array<Goal>>(`${API_URL}/student/goals`);
  }

  saveGoalTeacher(goal: Goal): Observable<any> {
    return this.http
      .post(`${API_URL}/teacher/goals/new`, goal);
  }

  saveGoalStudent(goal: Goal): Observable<any> {
    return this.http
      .post(`${API_URL}/student/goals/new`, goal);
  }

}
