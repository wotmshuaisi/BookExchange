import { Component, OnInit, Input } from '@angular/core';
import { DjangorestService } from 'src/app/djangorest.service';
import { FormControl, Validators, FormGroup, FormBuilder, FormControlName, ValidatorFn } from '@angular/forms';
import { RouterUtils } from 'src/app/utils/router';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less']
})
export class AppComponent {
  title = 'bookexchange';


  constructor(
    private usersSrv: DjangorestService,
    // private rUtils: RouterUtils,
  ) {
    // this.usersSrv.getsite().subscribe((res) => {
    //   this.title = res.title;
    // });

  }


}
