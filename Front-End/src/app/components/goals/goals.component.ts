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
    this.goalsListSubs = this.goalsApi
      .getGoals()
      .subscribe(res => {
          this.goalsList = res;
        },
        console.error
      );
  }

  ngOnDestroy() {
    this.goalsListSubs.unsubscribe();
  }

//   delete(TRIP_ID: number) {
//   this.tripsApi
//     .deleteTrip(TRIP_ID)
//     .subscribe(() => {
//       this.tripsListSubs = this.tripsApi
//         .getTrips()
//         .subscribe(res => {
//             this.tripsList = res;
//           },
//           console.error
//         );
//     }, console.error);
// }
}
