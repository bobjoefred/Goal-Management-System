import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import { catchError } from 'rxjs/operators';
import {API_URL} from '../env';
import {Teachers} from './teacher.model';

@Injectable()
export class TeachersApiService {

  constructor(private http: HttpClient) {
  }

  private static _handleError(err: HttpErrorResponse | any) {
    return Observable.throw(err.message || 'Error: Unable to complete request.');
  }

  // GET list of public, future events
  getTeachers():
  Observable<Array<Teacher>> {
    return this.http
    .get<Array<Teacher>>(`${API_URL}/teachers`);
    // .catchError(TripsApiService._handleError);
  }

//   saveTeacher(Teacher: Teacher): Observable<any> {
//   return this.http
//     .post(`${API_URL}/Teachers`, Teacher);
// }
}
