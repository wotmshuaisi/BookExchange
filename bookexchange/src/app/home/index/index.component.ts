import { Component, OnInit } from '@angular/core';
import { DjangorestService } from 'src/app/djangorest.service';
import { RouterUtils } from 'src/app/utils/router';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.less']
})
export class IndexComponent implements OnInit {
  announcement = '';
  guide = '';
  categorys: any;
  books: any;

  constructor(
    private usersSrv: DjangorestService,
    // private rUtils: RouterUtils,
    private activeRoute: ActivatedRoute,
  ) {
    this.usersSrv.getsite().subscribe((res) => {
      this.announcement = res.announcement;
      this.guide = res.guide;
    });
    this.usersSrv.getbookcategorys().subscribe((res) => {
      this.categorys = res;
    });

    let cid = 0;
    cid = this.activeRoute.snapshot.queryParams.cid;
    this.usersSrv.getbooks(cid, '', '').subscribe((res) => {
      this.books = res;
    });
    const search: string = this.activeRoute.snapshot.queryParams.search;
    if (search !== undefined && search.trim().length > 0) {
      this.usersSrv.getbooks(0, search, '').subscribe((res) => {
        this.books = res;
      });
    }
  }

  ngOnInit() {
  }

}
