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
    return this.http.post('/api/users/register/', { email: email, password: password }, { headers: this.defaultHeaders });
  }

  login(email: string, password: string): Observable<any> {
    return this.http.post('/api/users/login/', { email: email, password: password }, { headers: this.defaultHeaders });
  }

  logout(): Observable<any> {
    return this.http.get('/api/users/logout/');
  }

  getuser(): Observable<any> {
    return this.http.get('/api/users/');
  }

  getsite(): Observable<any> {
    return this.http.get('/api/siteinfo/');
  }

  getbookcategorys(): Observable<any> {
    return this.http.get('/api/category/');
  }

  getbooks(cid: number, s: string, id: string): Observable<any> {
    let uri = '/api/books/';
    if (cid >= 1) {
      uri = '/api/books/?category=' + cid;
    }
    if (s.length >= 1) {
      uri = '/api/books/?search=' + s;
    }

    if (id.length >= 1) {
      uri = '/api/books/' + id + '/';
    }

    return this.http.get(uri);
  }

  getmybooks(cid: number): Observable<any> {
    let uri = '/api/books/mybooks/';
    if (cid >= 1) {
      uri = '/api/books/mybooks/?cid=' + cid;
    }
    return this.http.get(uri);
  }

  getmarked(id: string, bid: string): Observable<any> {
    let uri = '/api/marked/';
    if (id !== '') {
      uri = '/api/marked/' + id + '/';
    }
    if (bid !== '') {
      uri = 'api/marked/?book=' + bid;
    }
    return this.http.get(uri);
  }

  setmark(bookid: number): Observable<any> {
    return this.http.post('/api/marked/', { book: bookid }, { headers: this.defaultHeaders });
  }

  unsetmark(id: number): Observable<any> {
    return this.http.delete('/api/marked/' + id + '/', { headers: this.defaultHeaders });
  }

  postbook(data): Observable<any> {
    return this.http.post('/api/books/', data, { headers: this.defaultHeaders });
  }

  getorders(uid: number): Observable<any> {
    let uri = '/api/orders/';
    if (uid > 0) {
      uri = uri + 'tome/?uid=' + uid;
    }
    return this.http.get(uri);
  }

  startorder(book: number, condition: number): Observable<any> {
    return this.http.post('/api/orders/start/', { book: book, condition: condition }, { headers: this.defaultHeaders });
  }

  exchange(id: string): Observable<any> {
    return this.http.post('/api/orders/exchange/', { order_id: id }, { headers: this.defaultHeaders });
  }

  uploadfile(data: FormData): Observable<any> {
    return this.http.post('/upload/', data);
  }

}
