import { Component, OnInit, Input } from '@angular/core';
import { DjangorestService } from 'src/app/djangorest.service';
import { FormControl, Validators, FormGroup, FormBuilder, FormControlName, ValidatorFn } from '@angular/forms';
import { RouterUtils } from 'src/app/utils/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.less']
})
export class RegisterComponent implements OnInit {
  @Input() formGroup: FormGroup;

  constructor(private formBuilder: FormBuilder,
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

    this.usersSrv.getuser().subscribe((res) => {
      if (res.email !== '') {
        window.alert('你已经是注册用户');
        this.rUtils.ToIndex();
        return;
      }
    });

  }

  ngOnInit() {
  }

  register() {


    if (this.formGroup.valid) {
      this.usersSrv.register(this.formGroup.get('email').value, this.formGroup.get('password').value).subscribe((res) => {
        if (res.status === true) {
          window.alert('注册成功');
          this.rUtils.ToLogin();
        } else {
          this.formGroup.setErrors({ err: res });
        }
      });
    }
  }

}
