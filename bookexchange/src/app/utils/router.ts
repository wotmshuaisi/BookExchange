import { Router } from '@angular/router';
import { Injectable } from '@angular/core';

@Injectable()
export class RouterUtils {
    LOGIN = '/login/';

    constructor(private r: Router) { }

    ToLogin() {
        this.r.navigateByUrl(this.LOGIN);
    }

    ToIndex() {
        this.r.navigateByUrl('/');
    }


}
