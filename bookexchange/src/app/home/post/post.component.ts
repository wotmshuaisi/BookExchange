import { Component, OnInit, Input } from '@angular/core';
import { RouterUtils } from 'src/app/utils/router';
import { DjangorestService } from 'src/app/djangorest.service';
import { FormBuilder, FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.less']
})
export class PostComponent implements OnInit {
  @Input() formGroup: FormGroup;
  categorys: any;

  constructor(
    private formBuilder: FormBuilder,
    private usersSrv: DjangorestService,
    private rUtils: RouterUtils,
  ) {
    this.formGroup = this.formBuilder.group({
      'title': new FormControl('', [
        Validators.required,
      ]),
      'wonder': new FormControl('', [
        Validators.required,
      ]),
      'category': new FormControl('', [
        Validators.required,
      ]),
      'page': new FormControl('', [
        Validators.required,
      ]),
      'price': new FormControl('', [
        Validators.required,
      ]),
      'month': new FormControl('', [
        Validators.required,
      ]),
      'boughtdate': new FormControl('', [
        Validators.required,
      ]),
      'quality': new FormControl('', [
        Validators.required,
      ]),
      'author': new FormControl('', [
        Validators.required,
      ]),
      'press': new FormControl('', [
        Validators.required,
      ]),
      'isbn': new FormControl('', [
        Validators.required,
      ]),
      'img': new FormControl('', [
        Validators.required,
      ]),
    });

    this.usersSrv.getuser().subscribe((res) => {
      if (res.email.length < 1) {
        this.rUtils.ToLogin();
      }
    });

    this.usersSrv.getbookcategorys().subscribe((res) => {
      this.categorys = res;
    });

  }

  ngOnInit() {
  }

  uploadfile(event) {
    const fileList: FileList = event.target.files;
    if (fileList.length > 0) {
      const f: File = fileList[0];
      const fd: FormData = new FormData();
      fd.append('file', f, f.name);
      this.usersSrv.uploadfile(fd).subscribe((res) => {
        if (res.success === true) {
          this.formGroup.get('img').setValue(res.path);
          console.log(this.formGroup.get('img').value);
        }
      });
    }
  }

  post() {
    console.log(this.formGroup.valid);
    console.log(this.formGroup.errors);

    if (this.formGroup.valid) {
      const data = {
        wonder: this.formGroup.get('wonder').value,
        title: this.formGroup.get('title').value,
        author: this.formGroup.get('author').value,
        press: this.formGroup.get('press').value,
        isbn: this.formGroup.get('isbn').value,
        month: this.formGroup.get('month').value,
        boughtdate: this.formGroup.get('boughtdate').value,
        category: this.formGroup.get('category').value,
        price: this.formGroup.get('price').value,
        page: this.formGroup.get('page').value,
        quality: this.formGroup.get('quality').value,
        img: this.formGroup.get('img').value,
      };
      console.log(data);
      this.usersSrv.postbook(data).subscribe(
        (res) => {
          window.alert('发布成功!');
          document.location.reload();
        },
        (err) => {
          window.alert('发布失败， 请重试!');
        }
      );
    }
  }

}
