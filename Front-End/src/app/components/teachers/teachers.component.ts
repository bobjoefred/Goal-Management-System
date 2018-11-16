import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs/Subscription';
import { Teacher } from './teacher.model';
import { TeachersApiService } from './teachers-api.service';

@Component({
  selector: 'app-teachers',
  templateUrl: './teachers.component.html',
  styleUrls: ['./teachers.component.css']
})
export class TeachersComponent implements OnInit {

  teachersListSubs: Subscription;
  teacherList: Teacher[];

  constructor(private teachersApi: TeachersApiService) { }

  ngOnInit() {
    this.teachersListSubs = this.teachersApi.getTeachers()
      .subscribe(result => {
        this.teacherList = result
      },
      console.error);
  }


  ngOnDestroy() {
    this.teachersListSubs.unsubscribe();
  }

}
