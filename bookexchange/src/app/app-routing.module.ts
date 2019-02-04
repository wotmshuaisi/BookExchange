import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { IndexComponent } from './home/index/index.component';
import { DetailComponent } from './home/detail/detail.component';
import { PostComponent } from './home/post/post.component';
import { RegisterComponent } from './home/register/register.component';
import { LoginComponent } from './home/login/login.component';
import { OrdersComponent } from './home/orders/orders.component';

const routes: Routes = [
  {
    path: '', component: HomeComponent,
    children: [
      { path: '', pathMatch: 'full', component: IndexComponent },
      { path: 'detail', component: DetailComponent },
      { path: 'post', component: PostComponent },
      { path: 'register', component: RegisterComponent },
      { path: 'login', component: LoginComponent },
      { path: 'orders', component: OrdersComponent },
    ]
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
