import { BrowserModule } from '@angular/platform-browser';
import { NgModule, Component } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { DetailComponent } from './home/detail/detail.component';
import { PostComponent } from './home/post/post.component';
import { IndexComponent } from './home/index/index.component';
import { LoginComponent } from './home/login/login.component';
import { RegisterComponent } from './home/register/register.component';
import { FormsModule, ReactiveFormsModule, } from '@angular/forms';
import { RouterUtils } from './utils/router';
import { HttpClientModule } from '@angular/common/http';
import { DjangorestService } from './djangorest.service';
import { OrdersComponent } from './home/orders/orders.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    DetailComponent,
    PostComponent,
    IndexComponent,
    LoginComponent,
    RegisterComponent,
    OrdersComponent,
    // FormsModule,
    // ReactiveFormsModule,
  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  providers: [
    RouterUtils,
    DjangorestService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
