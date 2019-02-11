import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import { API_URL } from '../../env';
import { Goal } from './goal.model';

@Injectable()
export class GoalsApiService {

  constructor(private http: HttpClient) {
  }

  private static _handleError(err: HttpErrorResponse | any) {
    return Observable.throw(err.message || 'Error: Unable to complete request.');
  }

  // GET list of public, future events
  createNewGoal(goal: Goal): Observable<any> {
    return this.http
    .post(`${API_URL}/teacher/goals/new`, goal);
  }

  getGoals():
  Observable<Array<Goal>> {
  return this.http
  .get<Array<Goal>>(`${API_URL}/teacher/goals`);
}

}
