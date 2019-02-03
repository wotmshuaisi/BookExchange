import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DjangorestService {
  defaultHeaders: HttpHeaders = new HttpHeaders({
    'Content-Type': 'application/json',
  });

  constructor(private http: HttpClient) { }

  register(email: string, password: string): Observable<any> {
    return this.http.post('/api/users/', { email: email, password: password }, { headers: this.defaultHeaders });
  }

  // register(email: string, password: string): Observable<any> {
  //   return this.http.post('/api/users/', { email: email, password: password }, { headers: this.defaultHeaders });
  // }

}
