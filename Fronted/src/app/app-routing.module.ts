import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PrincipalComponent } from './paginas/principal/principal.component';
import { LoginComponent } from './paginas/login/login.component';

const routes: Routes = [
  {
    path: "principal", 
    component: PrincipalComponent
  },
  {
    path: "login", 
    component: LoginComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
