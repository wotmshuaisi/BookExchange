import { Component, OnInit, Input } from '@angular/core';
import { DjangorestService } from '../djangorest.service';
import { RouterUtils } from '../utils/router';
import { FormGroup, FormBuilder, Validators, FormControl } from '@angular/forms';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.less']
})
export class HomeComponent implements OnInit {
  @Input() formGroup: FormGroup;
  email = '';
  announcement = '';
  guide = '';
  title = '';
  count = 0;

  constructor(
    private formBuilder: FormBuilder,
    private usersSrv: DjangorestService,
    private rUtils: RouterUtils,
  ) {
    this.formGroup = this.formBuilder.group({
      'search': new FormControl('', [
        Validators.required,
      ]),
    });

    this.usersSrv.getuser().subscribe((res) => {
      if (res.email !== '') {
        this.email = res.email;
      }
    });
    this.usersSrv.getsite().subscribe((res) => {
      this.announcement = res.announcement;
      this.guide = res.guide;
      this.title = res.title;
    });
    this.usersSrv.getmarked('', '').subscribe((res) => {
      this.count = res.length;
    });
  }


  ngOnInit() {
  }

  logout() {
    this.usersSrv.logout().subscribe((res) => {
      window.alert('注销成功');
      document.location.href = '/';
    });
  }

  search() {
    window.location.href = '/?search=' + this.formGroup.get('search').value;
  }

}
