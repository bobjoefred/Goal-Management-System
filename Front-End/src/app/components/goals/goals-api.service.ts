import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { API_URL } from '../../env';
import { Goal } from './goal.model';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class GoalsApiService {

  constructor(readonly http: HttpClient) {
  }

  static _handleError(err: HttpErrorResponse | any): Observable<any> {
    return Observable
    .throw(err.message || 'Error: Unable to complete request.');
  }

  deleteGoalTeacher(GOAL_ID: number): Observable<any> {
    return this.http
      .delete(`${API_URL}/teacher/goals/${GOAL_ID}/delete`);
  }

  deleteGoalStudent(GOAL_ID: number): Observable<any> {
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
