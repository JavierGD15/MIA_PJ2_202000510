import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { CodemirrorModule } from '@ctrl/ngx-codemirror';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PrincipalComponent } from './paginas/principal/principal.component';
import { HttpClientModule } from '@angular/common/http';
import { DevExtremeModule } from 'devextreme-angular';
import { LoginComponent } from './paginas/login/login.component';

import { MatCardModule } from '@angular/material/card';

import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';

@NgModule({
  declarations: [
    AppComponent,
    PrincipalComponent,
    LoginComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    NoopAnimationsModule,
    DevExtremeModule, 
    FormsModule,
    CodemirrorModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
