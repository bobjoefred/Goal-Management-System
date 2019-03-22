import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { catchError } from 'rxjs/operators';
import { API_URL } from '../../env';
import { Teacher } from './teacher.model';
import { Goal } from '../goals/goal.model';

@Injectable()
export class TeachersApiService {

  constructor(private readonly http: HttpClient) {
  }

  // GET list of public, future events
  getTeachers():
  Observable<Array<Teacher>> {
    return this.http
    .get<Array<Teacher>>(`${API_URL}/teachers`);
  }

  createNewGoal(goal: Goal): Observable<any> {
    return this.http
    .post(`${API_URL}/teacher/goals/new`, goal);
  }

}
