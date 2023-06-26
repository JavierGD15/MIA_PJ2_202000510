import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { login } from 'src/app/models/login';
import { AnalisisService } from 'src/app/services/analisis.service';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {


  constructor(private formBuilder:FormBuilder,private log: AnalisisService, private router: Router) { }

  formularioLogin: FormGroup = this.formBuilder.group({
    usuario: ['', [Validators.required]],
    contra: ['', [Validators.required]]
  })

  persona: login = {
    usuario: '',
    password: ''
    };
  usuario: string = '';
  contra: string = '';
  
  loger: string = '';

  ngOnInit() {
  }

  onSubmit() {
    if (this.formularioLogin.valid) {
      console.log(this.formularioLogin.value);
      this.enviar();
    }
  }

  getUsuarioValido() {
    return this.usuario = this.formularioLogin.get('usuario')?.value;
  }

  getContraValida() {
    return this.contra = this.formularioLogin.get('contra')?.value;
  }

  get noUsuario() {
    return this.formularioLogin.get('usuario');
  }

  get noContra() {
    return this.formularioLogin.get('contra');
  }


  enviar() {
    this.persona.usuario = this.getUsuarioValido();
    this.persona.password = this.getContraValida();
    this.log.login(this.persona).subscribe(
      (res) => {
        console.log(res);
        this.loger = res.salida;
        console.log(this.loger);
        var resultado = this.loger;
        if (resultado == "True") {
          this.router.navigate(['/principal']);
        }
        else {
          console.log("no entros");
        }
      },
      (err) => {
        console.log(err);
      }
    );
  }
}
