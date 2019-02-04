import { Component, OnInit, Input } from '@angular/core';
import { DjangorestService } from 'src/app/djangorest.service';
import { FormControl, Validators, FormGroup, FormBuilder, FormControlName, ValidatorFn } from '@angular/forms';
import { RouterUtils } from 'src/app/utils/router';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.less']
})
export class LoginComponent implements OnInit {
  @Input() formGroup: FormGroup;


  constructor(
    private formBuilder: FormBuilder,
    private usersSrv: DjangorestService,
    private rUtils: RouterUtils,
  ) {
    this.formGroup = this.formBuilder.group({
      'email': new FormControl('', [
        Validators.required,
        Validators.email,
      ]),
      'password': new FormControl('', [
        Validators.required,
      ])
    });

  }

  ngOnInit() {
  }

  login() {
    if (this.formGroup.valid) {
      this.usersSrv.login(this.formGroup.get('email').value, this.formGroup.get('password').value).subscribe((res) => {
        if (res.status === true) {
          this.rUtils.ToIndex();
        } else {
          this.formGroup.setErrors({ err: 'incorrect email or password' });
        }
      });
    }
  }
}
