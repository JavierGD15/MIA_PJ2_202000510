import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {


  constructor(private formBuilder:FormBuilder) { }

  formularioLogin: FormGroup = this.formBuilder.group({
    usuario: ['', [Validators.required]],
    contra: ['', [Validators.required]]
  })

  usuario: string = '';
  contra: string = '';

  ngOnInit() {
  }

  onSubmit() {
    if (this.formularioLogin.valid) {
      console.log(this.formularioLogin.value);
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
}
