import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import  salida  from 'src/app/models/salida';

@Injectable({
    providedIn: 'root'
  })
  export class AnalisisService {
    url = 'http://localhost:8000/';
    // url = 'https://agile-basin-94607.herokuapp.com/';
    constructor(private httpClient: HttpClient) { }

    interpretar(data:any){
      return this.httpClient.post<salida>(this.url+'interpretar',data);
    }

    login(data:any){
      return this.httpClient.post<salida>(this.url+'login',data);
    }
  }
  