import { Component, OnInit, Input } from '@angular/core';
import { RouterUtils } from 'src/app/utils/router';
import { DjangorestService } from 'src/app/djangorest.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.less']
})
export class OrdersComponent implements OnInit {
  myorders: any;
  tomeorders: any;

  constructor(
    private activeRoute: ActivatedRoute,
    private usersSrv: DjangorestService,
    private rUtils: RouterUtils,
  ) {
    this.usersSrv.getuser().subscribe((res) => {
      if (res.email.length < 1) {
        this.rUtils.ToLogin();
      }
      this.updatetomeorders(res.id);
    });

    this.usersSrv.getorders(0).subscribe((res) => {
      this.myorders = res;
      for (let index = 0; index < this.myorders.length; index++) {
        this.getbookinfo(index, false);
      }
      // console.log('1');
      console.log(this.myorders);

    });

  }

  updatetomeorders(uid: number) {
    this.usersSrv.getorders(uid).subscribe((res) => {
      this.tomeorders = res;
      for (let index = 0; index < this.tomeorders.length; index++) {
        this.getbookinfo(index, true);

      }
    });
  }

  getbookinfo(index: number, to: boolean) {
    if (!to) {
      this.usersSrv.getbooks(0, '', this.myorders[index].book.toString()).subscribe((res) => {
        this.myorders[index].bv = res;
      });
      this.usersSrv.getbooks(0, '', this.myorders[index].condition.toString()).subscribe((res) => {
        this.myorders[index].obv = res;
      });
    } else {
      console.log(this.tomeorders);
      this.usersSrv.getbooks(0, '', this.tomeorders[index].book_id.toString()).subscribe((res) => {
        this.tomeorders[index].bv = res;
      });
      this.usersSrv.getbooks(0, '', this.tomeorders[index].condition.toString()).subscribe((res) => {
        this.tomeorders[index].obv = res;
      });
    }
  }

  ngOnInit() {
  }

  confirm(oid: string) {
    this.usersSrv.getuser().subscribe((res) => {
      if (res.email.length < 1) {
        this.rUtils.ToLogin();
      }
    });
    this.usersSrv.exchange(oid).subscribe(
      (res) => {
        window.alert('确认成功!');
        window.location.reload();
      },
      (err) => {
        window.alert('确认失败，请联系管理员');
        window.location.reload();
      }
    );
  }

}
