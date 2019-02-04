import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { RouterUtils } from 'src/app/utils/router';
import { DjangorestService } from 'src/app/djangorest.service';
import { Validators, FormBuilder, FormControl, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.less']
})
export class DetailComponent implements OnInit {
  @Input() formGroup: FormGroup;
  book: any;
  id: string;
  marked = false;
  mid: number;
  condition = true;
  email = 0;
  mybook: any;
  constructor(
    private formBuilder: FormBuilder,
    private activeRoute: ActivatedRoute,
    private usersSrv: DjangorestService,
    private rUtils: RouterUtils,
  ) {

    this.formGroup = this.formBuilder.group({
      'b': new FormControl('', [
        Validators.required,
      ]),
    });

    this.id = this.activeRoute.snapshot.queryParams.id;
    if (this.id.length <= 0) {
      this.rUtils.ToIndex();
      return;
    }
    this.usersSrv.getuser().subscribe(
      (data) => {
        this.email = data.email;
      },
    );

    this.usersSrv.getmarked('', this.id).subscribe((res) => {
      if (res.length !== 0) {
        this.marked = true;
        this.mid = res[0].id;
      }
    });

    this.usersSrv.getbooks(0, '', this.id).subscribe((res) => {
      this.book = res;
      switch (res.quality) {
        case 1:
          this.book.quality = '9成';
          break;
        case 2:
          this.book.quality = '8成';
          break;
        case 3:
          this.book.quality = '7成及以下';
          break;
        default:
          this.book.quality = '未知';
          break;
      }
      if (this.book.user_email === this.email) {
        this.condition = false;
      }
      if (!this.book.available) {
        this.condition = false;
      }
      this.getmybook();
    });



  }

  getmybook() {
    this.usersSrv.getmybooks(this.book.category_id).subscribe((res) => {
      if (res.length < 1) {
        this.condition = false;
      }
      this.mybook = res;
    });
  }

  ngOnInit() {

  }

  mark() {
    this.usersSrv.getuser().subscribe((res) => {
      if (res.email.length < 1) {
        this.rUtils.ToLogin();
      }
    });

    this.usersSrv.setmark(parseInt(this.id, 10)).subscribe((res) => {
      document.location.reload();
    });

  }

  unmark() {
    this.usersSrv.getuser().subscribe((res) => {
      if (res.email.length < 1) {
        this.rUtils.ToLogin();
      }
    });

    this.usersSrv.unsetmark(this.mid).subscribe((res) => {
      document.location.reload();
    });

  }

  post() {
    this.usersSrv.getuser().subscribe((res) => {
      if (res.email.length < 1) {
        this.rUtils.ToLogin();
      }
    });
    if (this.formGroup.valid) {
      const bid: string = this.formGroup.get('b').value;
      this.usersSrv.startorder(parseInt(this.id, 10), parseInt(bid, 10)).subscribe(
        (res) => {
          window.alert('发起成功');
          window.location.href = '/orders/';
        },
        (err) => {
          window.alert('发起失败');
          window.location.reload();
        }
      );
    }
  }

}
